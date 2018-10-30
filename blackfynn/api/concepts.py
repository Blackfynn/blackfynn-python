# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from future.utils import string_types

import requests

from blackfynn.api.base import APIBase
from blackfynn.models import (
    DataPackage,
    GraphViewDefinition,
    GraphViewSnapshot,
    Model,
    ModelProperty,
    ModelTemplate,
    ProxyInstance,
    Record,
    RecordSet,
    Relationship,
    RelationshipProperty,
    RelationshipSet,
    RelationshipType
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ModelsAPIBase(APIBase):

    def _get_concept_type(self, concept, instance = None):
        if isinstance(concept, Model):
            return concept.type
        elif isinstance(concept, string_types):
            return concept
        elif isinstance(instance, Record):
            return instance.type
        else:
            raise Exception("could not get concept type from concept {} or instance {} ".format(concept, instance))

    def _get_relationship_type(self, relationship, instance = None):
        if isinstance(relationship, RelationshipType):
            return relationship.type
        elif isinstance(relationship, string_types):
            return relationship
        elif isinstance(instance, Relationship):
            return instance.type
        else:
            raise Exception("could not get relationship type from relationship {} or instance {} ".format(relationship, instance))


class ModelsAPI(ModelsAPIBase):
    base_uri = "/datasets"
    name = 'concepts'

    def __init__(self, session):
        self.host = session._concepts_host
        self.instances = RecordsAPI(session)
        self.relationships = ModelRelationshipsAPI(session)
        self.proxies = ModelProxiesAPI(session)
        super(ModelsAPI, self).__init__(session)

    def get_properties(self, dataset, concept):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        resp = self._get(self._uri('/{dataset_id}/concepts/{id}/properties', dataset_id=dataset_id, id=concept_id))
        return [ModelProperty.from_dict(r) for r in resp]

    def update_properties(self, dataset, concept):
        assert isinstance(concept, Model), "concept must be type Model"
        assert concept.schema, "concept schema cannot be empty"
        data = concept.as_dict()['schema']
        dataset_id = self._get_id(dataset)
        resp = self._put(self._uri('/{dataset_id}/concepts/{id}/properties', dataset_id=dataset_id, id=concept.id), json=data)
        return [ModelProperty.from_dict(r) for r in resp]

    def delete_property(self, dataset, concept, prop):
        dataset_id  = self._get_id(dataset)
        concept_id  = self._get_id(concept)
        property_id = self._get_id(prop)
        return self._del(self._uri('/{dataset_id}/concepts/{concept_id}/properties/{property_id}',
                dataset_id  = dataset_id,
                concept_id  = concept_id,
                property_id = property_id))

    def get(self, dataset, concept):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        r = self._get(self._uri('/{dataset_id}/concepts/{id}', dataset_id=dataset_id, id=concept_id))
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        r['schema'] = self.get_properties(dataset, concept)
        return Model.from_dict(r, api=self.session)

    def delete(self, dataset, concept):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        return self._del(self._uri('/{dataset_id}/concepts/{id}', dataset_id=dataset_id, id=concept.id))

    def update(self, dataset, concept):
        assert isinstance(concept, Model), "concept must be type Model"
        data = concept.as_dict()
        data['id'] = concept.id
        dataset_id = self._get_id(dataset)
        r = self._put(self._uri('/{dataset_id}/concepts/{id}', dataset_id=dataset_id, id=concept.id), json=data)
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        if concept.schema:
            r['schema'] = self.update_properties(dataset, concept)
        return Model.from_dict(r, api=self.session)

    def create(self, dataset, concept):
        assert isinstance(concept, Model), "concept must be type Model"
        dataset_id = self._get_id(dataset)
        r = self._post(self._uri('/{dataset_id}/concepts', dataset_id=dataset_id), json=concept.as_dict())
        concept.id = r['id']
        r['dataset_id'] = r.get('dataset_id', dataset_id)

        if concept.schema:
            try:
                r['schema'] = self.update_properties(dataset, concept)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 400:
                    self._logger.error(
                        "Model was successfully created, but properties were "
                        "rejected with the following error: {}".format(str(
                            e.response.text.split('\n')[0]
                        ))
                    )
                else:
                    raise

        return Model.from_dict(r, api=self.session)

    def get_all(self, dataset):
        dataset_id = self._get_id(dataset)
        resp = self._get(self._uri('/{dataset_id}/concepts', dataset_id=dataset_id), stream=True)
        for r in resp:
            r['dataset_id'] = r.get('dataset_id', dataset_id)
            r['schema'] = self.get_properties(dataset, r['id'])
        concepts = [Model.from_dict(r, api=self.session) for r in resp]
        return { c.type: c for c in concepts }

    def delete_instances(self, dataset, concept, *instances):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        ids = [self._get_id(instance) for instance in instances]

        return self._del(self._uri('/{dataset_id}/concepts/{id}/instances', dataset_id=dataset_id, id=concept_id), json=ids)

    def files(self, dataset, concept, instance):
        """
        Return list of files (i.e. packages) related to record.
        """
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        instance_id = self._get_id(instance)
        resp = self._get(
            self._uri('/{dataset_id}/concepts/{concept_id}/instances/{instance_id}/files',
                dataset_id=dataset_id,
                concept_id=concept_id,
                instance_id=instance_id
            ))
        return [DataPackage.from_dict(pkg, api=self.session) for r,pkg in resp]

    def get_related(self, dataset, concept):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        resp = self._get(
            self._uri('/{dataset_id}/concepts/{concept_id}/topology',
                      dataset_id=dataset_id, concept_id=concept_id))
        for r in resp:
            r['dataset_id'] = r.get('dataset_id', dataset_id)
            r['schema'] = self.get_properties(dataset, r['id'])
        concepts = [Model.from_dict(r, api=self.session) for r in resp]

        return concepts

    def get_topology(self, dataset):
        dataset_id = self._get_id(dataset)
        resp = self._get(
            self._uri('/{dataset_id}/concepts/schema/graph',
                      dataset_id=dataset_id))
        # What is returned is a list mixing
        results = {
            'models': [],
            'relationships': []
        }
        for r in resp:
            r['dataset_id'] = r.get('dataset_id', dataset_id)
            if 'from' in r:
                # This is a relationship
                results['relationships'].append(
                    Relationship.from_dict(r, api=self.session))
            else:
                # This is a model
                r['schema'] = self.get_properties(dataset, r['id'])
                results['models'].append(Model.from_dict(r, api=self.session))
        return results

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Model Instances
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RecordsAPI(ModelsAPIBase):
    base_uri = "/datasets"
    name = 'concepts.instances'

    def __init__(self, session):
        self.host = session._concepts_host
        super(RecordsAPI, self).__init__(session)

    def get(self, dataset, instance, concept=None):
        dataset_id = self._get_id(dataset)
        instance_id = self._get_id(instance)
        concept_type = self._get_concept_type(concept, instance)

        r = self._get(self._uri('/{dataset_id}/concepts/{concept_type}/instances/{id}', dataset_id=dataset_id, concept_type=concept_type, id=instance_id))
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        return Record.from_dict(r, api=self.session)

    def relations(self, dataset, instance, related_concept, concept=None):
        dataset_id = self._get_id(dataset)
        instance_id = self._get_id(instance)
        related_concept_type = self._get_id(related_concept)
        concept_type = self._get_concept_type(concept, instance)

        res = self._get(self._uri('/{dataset_id}/concepts/{concept_type}/instances/{id}/relations/{related_concept_type}', dataset_id=dataset_id, concept_type=concept_type, id=instance_id, related_concept_type=related_concept_type))

        relations = []
        for r in res:
            relationship = r[0]
            concept = r[1]

            relationship['dataset_id'] = relationship.get('dataset_id', dataset_id)
            concept['dataset_id'] = concept.get('dataset_id', dataset_id)

            relationship = Relationship.from_dict(relationship, api=self.session)
            concept = Record.from_dict(concept, api=self.session)

            relations.append((relationship, concept))

        return relations

    def get_all(self, dataset, concept, limit=100, offset=0):
        dataset_id = self._get_id(dataset)
        concept_type = self._get_concept_type(concept)

        resp = self._get(self._uri('/{dataset_id}/concepts/{concept_type}/instances', dataset_id=dataset_id, concept_type=concept_type), params=dict(limit=limit, offset=offset), stream=True)
        for r in resp:
          r['dataset_id'] = r.get('dataset_id', dataset_id)
        instances = [Record.from_dict(r, api=self.session) for r in resp]

        return RecordSet(concept, instances)

    def delete(self, dataset, instance):
        assert isinstance(instance, Record), "instance must be type Record"
        dataset_id = self._get_id(dataset)
        return self._del(self._uri(
            '/{dataset_id}/concepts/{concept_type}/instances/{id}',
            dataset_id=dataset_id, concept_type=instance.type,
            id=instance.id
        ))

    def create(self, dataset, instance):
        assert isinstance(instance, Record), "instance must be type Record"
        dataset_id = self._get_id(dataset)
        r = self._post(self._uri('/{dataset_id}/concepts/{concept_type}/instances', dataset_id=dataset_id, concept_type=instance.type), json=instance.as_dict())
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        return Record.from_dict(r, api=self.session)

    def update(self, dataset, instance):
        assert isinstance(instance, Record), "instance must be type Record"
        dataset_id = self._get_id(dataset)
        r = self._put(self._uri('/{dataset_id}/concepts/{concept_type}/instances/{id}', dataset_id=dataset_id, concept_type=instance.type, id=instance.id), json=instance.as_dict())
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        return Record.from_dict(r, api=self.session)

    def create_many(self, dataset, concept, *instances):
        instance_type = instances[0].type
        for inst in instances:
            assert isinstance(inst, Record), "instance must be type Record"
            assert inst.type == instance_type, "Expected instance of type {}, found instance of type {}".format(instance_type, inst.type)
        dataset_id = self._get_id(dataset)
        values = [inst.as_dict() for inst in instances]
        resp = self._post(self._uri('/{dataset_id}/concepts/{concept_type}/instances/batch', dataset_id=dataset_id, concept_type=instance_type), json=values, stream=True)

        for r in resp:
            r['dataset_id'] = r.get('dataset_id', dataset_id)
        instances = [Record.from_dict(r, api=self.session) for r in resp]
        return RecordSet(concept, instances)

    def get_all_related(self, dataset, source_instance):
        related = self.get_counts(dataset, source_instance)
        return {
            item['name']: self.get_all_related_of_type(dataset, source_instance, item['name'])
            for item in related
            if not (item['name']=='package' and item['displayName']=='Files')
            # ^^ TODO: have API provide better means of distinguishing proxy vs. model
        }

    def get_all_related_of_type(self, dataset, source_instance, return_type, source_concept=None):
        """
        Return all records of type return_type related to instance.
        """
        dataset_id   = self._get_id(dataset)
        instance_id  = self._get_id(source_instance)
        instance_type = self._get_concept_type(source_concept, source_instance)
        resp = self._get(self._uri('/{dataset_id}/concepts/{instance_type}/instances/{instance_id}/relations/{return_type}',
                    dataset_id    = dataset_id,
                    instance_type = instance_type,
                    instance_id   = instance_id,
                    return_type   = return_type))
        for edge,node in resp:
            node['dataset_id'] = node.get('dataset_id', dataset_id)
        if not isinstance(return_type, Model):
            return_type = self.session.concepts.get(dataset, return_type)
        records = [Record.from_dict(r, api=self.session) for _,r in resp]
        return RecordSet(return_type, records)

    def get_counts(self, dataset, instance, concept=None):
        dataset_id   = self._get_id(dataset)
        concept_type = self._get_concept_type(concept, instance)
        instance_id  = self._get_id(instance)
        return self._get(self._uri('/{dataset_id}/concepts/{concept_type}/instances/{instance_id}/relationCounts',
                    dataset_id   = dataset_id,
                    concept_type = concept_type,
                    instance_id  = instance_id))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Relationships
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ModelRelationshipsAPI(ModelsAPIBase):
    base_uri = "/datasets"
    name = 'concepts.relationships'

    def __init__(self, session):
        self.host = session._concepts_host
        self.instances = ModelRelationshipInstancesAPI(session)
        super(ModelRelationshipsAPI, self).__init__(session)

    def create(self, dataset, relationship):
        assert isinstance(relationship, RelationshipType), "Must be of type Relationship"
        dataset_id = self._get_id(dataset)
        r = self._post(self._uri('/{dataset_id}/relationships', dataset_id=dataset_id), json=relationship.as_dict())
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        return RelationshipType.from_dict(r, api=self.session)

    def get(self, dataset, relationship):
        dataset_id = self._get_id(dataset)
        relationship_id = self._get_id(relationship)
        r = self._get(self._uri('/{dataset_id}/relationships/{r_id}', dataset_id=dataset_id, r_id=relationship_id))
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        return RelationshipType.from_dict(r, api=self.session)

    def get_all(self, dataset):
        dataset_id = self._get_id(dataset)
        resp = self._get(self._uri('/{dataset_id}/relationships', dataset_id=dataset_id), stream=True)
        for r in resp:
          r['dataset_id'] = r.get('dataset_id', dataset_id)
        relations = [RelationshipType.from_dict(r, api=self.session) for r in resp]
        return {r.type: r for r in relations}

class ModelRelationshipInstancesAPI(ModelsAPIBase):
    base_uri = "/datasets"
    name = 'concepts.relationships.instances'

    def __init__(self, session):
        self.host = session._concepts_host
        super(ModelRelationshipInstancesAPI, self).__init__(session)

    def get_all(self, dataset, relationship):
        dataset_id = self._get_id(dataset)
        relationship_id = self._get_id(relationship)

        resp = self._get(self._uri('/{dataset_id}/relationships/{r_id}/instances', dataset_id=dataset_id, r_id=relationship_id), stream=True)
        for r in resp:
          r['dataset_id'] = r.get('dataset_id', dataset_id)
        instances = [Relationship.from_dict(r, api=self.session) for r in resp]
        return RelationshipSet(relationship, instances)

    def get(self, dataset, instance, relationship=None):
        dataset_id = self._get_id(dataset)
        instance_id = self._get_id(instance)
        relationship_type = self._get_relationship_type(relationship, instance)
        r = self._get( self._uri('/{dataset_id}/relationships/{r_type}/instances/{id}', dataset_id=dataset_id, r_type=relationship_type, id=instance_id))
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        return Relationship.from_dict(r, api=self.session)

    def delete(self, dataset, instance):
        assert isinstance(instance, Relationship), "instance must be of type Relationship"
        dataset_id = self._get_id(dataset)
        return self._del( self._uri('/{dataset_id}/relationships/{r_type}/instances/{id}', dataset_id=dataset_id, r_type=instance.type, id=instance.id))

    def link(self, dataset, relationship, source, destination, values=dict()):
        assert isinstance(source, (Record, DataPackage)), "source must be an object of type Record or DataPackage"
        assert isinstance(destination, (Record, DataPackage)), "destination must be an object of type Record or DataPackage"

        if isinstance(source, DataPackage):
            assert isinstance(destination, Record), "DataPackages can only be linked to Records"
            return self.session.concepts.proxies.create(dataset, source.id, relationship, destination, values, "ToTarget", "package")
        elif isinstance(destination, DataPackage):
            assert isinstance(source, Record), "DataPackages can only be linked to Records"
            return self.session.concepts.proxies.create(dataset, destination.id, relationship, source, values, "FromTarget", "package")
        else:
            dataset_id = self._get_id(dataset)
            relationship_type = self._get_relationship_type(relationship)
            values = [dict(name=k, value=v) for k,v in values.items()]
            instance = Relationship(dataset_id=dataset_id, type=relationship_type, source=source, destination=destination, values=values)
            return self.create(dataset, instance)

    def create(self, dataset, instance):
        assert isinstance(instance, Relationship), "instance must be of type Relationship"
        dataset_id = self._get_id(dataset)
        resp = self._post( self._uri('/{dataset_id}/relationships/{r_type}/instances', dataset_id=dataset_id, r_type=instance.type), json=instance.as_dict())
        r = resp[0] # responds with list
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        return Relationship.from_dict(r, api=self.session)

    def create_many(self, dataset, relationship, *instances):
        assert all([isinstance(i, Relationship) for i in instances]), "instances must be of type Relationship"
        instance_type = instances[0].type
        dataset_id = self._get_id(dataset)
        values = [inst.as_dict() for inst in instances]
        resp = self._post( self._uri('/{dataset_id}/relationships/{r_type}/instances/batch', dataset_id=dataset_id, r_type=instance_type), json=values)

        for r in resp:
            r[0]['dataset_id'] = r[0].get('dataset_id', dataset_id)
        instances =  [Relationship.from_dict(r[0], api=self.session) for r in resp]
        return RelationshipSet(relationship, instances)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Model Proxies
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ModelProxiesAPI(ModelsAPIBase):
    base_uri = "/datasets"
    name = 'concepts.proxies'

    proxy_types = ["package"]
    direction_types = ["FromTarget", "ToTarget"]

    def __init__(self, session):
        self.host = session._concepts_host
        super(ModelProxiesAPI, self).__init__(session)

    def get_all(self, dataset, proxy_type):
        dataset_id = self._get_id(dataset)
        r = self._get(self._uri('/{dataset_id}/proxy/{p_type}/instances', dataset_id=dataset_id, p_type=proxy_type))
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        return r

    def get(self, dataset, proxy_type, proxy_id):
        dataset_id = self._get_id(dataset)
        r = self._get(self._uri('/{dataset_id}/proxy/{p_type}/instances/{p_id}', dataset_id=dataset_id, p_type=proxy_type, p_id=proxy_id))
        r['dataset_id'] = r.get('dataset_id', dataset_id)
        return r

    def create(self, dataset, external_id, relationship, concept_instance, values, direction = "ToTarget", proxy_type = "package", concept = None):
        assert proxy_type in self.proxy_types, "proxy_type must be one of {}".format(self.proxy_types)
        assert direction in self.direction_types, "direction must be one of {}".format(self.direction_types)

        dataset_id = self._get_id(dataset)
        concept_instance_id = self._get_id(concept_instance)
        concept_type = self._get_concept_type(concept, concept_instance)
        relationship_type = self._get_relationship_type(relationship)
        relationshipData = [dict(name=k, value=v) for k,v in values.items()]

        request = {}
        request['externalId'] = external_id
        request['conceptType'] = concept_type
        request['conceptInstanceId'] = concept_instance_id
        request['targets'] = [
            {
                'direction': direction,
                'linkTarget': {
                    "ConceptInstance": {
                        'id': concept_instance_id
                    }
                },
                'relationshipType': relationship_type,
                'relationshipData': relationshipData
            }
        ]

        r = self._post(self._uri('/{dataset_id}/proxy/{p_type}/instances', dataset_id=dataset_id, p_type=proxy_type), json=request)
        instance = r[0]['relationshipInstance']
        instance['dataset_id'] = instance.get('dataset_id', dataset_id)
        return Relationship.from_dict(instance, api=self.session)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Model Templates
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ModelTemplatesAPI(APIBase):

    base_uri = "/model-schema"
    name = 'templates'

    def get_all(self):
        org_id = self._get_int_id(self.session._context)
        resp = self._get(self._uri('/organizations/{orgId}/templates', orgId=org_id))
        return [ModelTemplate.from_dict(t) for t in resp]

    def get(self, template_id):
        org_id = self._get_int_id(self.session._context)
        resp = self._get(self._uri('/organizations/{orgId}/templates/{templateId}',
                                   orgId=org_id, templateId=template_id))
        return ModelTemplate.from_dict(resp)

    def validate(self, template):
        assert isinstance(template, ModelTemplate), "template must be type Template"
        response = self._post(self._uri('/validate'), json=template.as_dict())
        if response == "":
            return True
        else:
            return response

    def create(self, template):
        assert isinstance(template, ModelTemplate), "template must be type Template"
        org_id = self._get_int_id(self.session._context)
        resp = self._post(self._uri('/organizations/{orgId}/templates', orgId=org_id), json=template.as_dict())
        return ModelTemplate.from_dict(resp)

    def apply(self, dataset, template):
        org_id = self._get_int_id(self.session._context)
        dataset_id = self._get_int_id(dataset)
        template_id = self._get_id(template)
        resp = self._post(self._uri('/organizations/{orgId}/templates/{templateId}/datasets/{datasetId}',
                                    orgId=org_id, templateId=template_id, datasetId=dataset_id))
        return [ModelProperty.from_dict(t) for t in resp]

    def delete(self, template_id):
        org_id = self._get_int_id(self.session._context)
        return self._del(self._uri('/organizations/{orgId}/templates/{templateId}',
                                   orgId=org_id, templateId=template_id))



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Graph Views
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def _with_dataset(resp, dataset):
    resp['dataset'] = dataset
    resp['dataset_id'] = dataset.id
    return resp


class AnalyticsAPI(APIBase):
    base_uri = '/analytics'
    name = 'analytics'

    def _kwargs(self, dataset, view=None, instance=None, **kwargs):
        kwargs.update({
            'orgId': self._get_int_id(self.session._context),
            'datasetId': self._get_int_id(dataset)
        })

        if view is not None:
            kwargs['graphViewId'] = self._get_id(view)

        if instance is not None:
            kwargs['graphViewInstanceId'] = self._get_id(instance)

        return kwargs

    def create_view(self, dataset, name, root, include):
        uri = self._uri('/organizations/{orgId}/datasets/{datasetId}/views',
                        **self._kwargs(dataset))

        try:
            resp = self._post(uri, json={
                'name': name,
                'rootModel': root,
                'includedModels': include,
            })
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise Exception(e.response.text)
            else:
                raise

        resp = _with_dataset(resp, dataset)
        return GraphViewDefinition.from_dict(resp, api=self.session)

    def get_view(self, dataset, view):
        uri = self._uri('/organizations/{orgId}/datasets/{datasetId}/views/{graphViewId}',
                        **self._kwargs(dataset, view))
        resp = self._get(uri)
        resp = _with_dataset(resp, dataset)
        return GraphViewDefinition.from_dict(resp, api=self.session)

    def delete_view(self, view):
        uri = self._uri('/organizations/{orgId}/datasets/{datasetId}/views/{graphViewId}',
                        **self._kwargs(view.dataset, view))
        return self._del(uri)

    def get_all_views(self, dataset):
        uri = self._uri('/organizations/{orgId}/datasets/{datasetId}/views',
                        **self._kwargs(dataset))
        resp = self._get(uri)
        return [GraphViewDefinition.from_dict(_with_dataset(r, dataset), api=self.session) for r in resp]

    def create_view_instance(self, view, batch_size=100):
        uri = self._uri('/organizations/{orgId}/datasets/{datasetId}/views/{graphViewId}/instances?batchSize={batch_size}',
                        batch_size=batch_size,
                        **self._kwargs(view.dataset, view))
        resp = self._post(uri)
        resp = _with_dataset(resp, view.dataset)
        resp['view'] = view
        return GraphViewSnapshot.from_dict(resp, api=self.session)

    def get_view_instance(self, view, instance_id):
        uri = self._uri('/organizations/{orgId}/datasets/{datasetId}/views/instances/{graphViewInstanceId}',
                        **self._kwargs(view.dataset, instance=instance_id))
        resp = self._get(uri)
        resp['view'] = view
        _with_dataset(resp, view.dataset)
        return GraphViewSnapshot.from_dict(resp, api=self.session)

    def get_all_view_instances(self, view):
        uri = self._uri('/organizations/{orgId}/datasets/{datasetId}/views/{graphViewId}/instances',
                        **self._kwargs(view.dataset, view))
        resp = self._get(uri)
        for r in resp:
            r['view'] = view
            _with_dataset(r, view.dataset)
        return [GraphViewSnapshot.from_dict(r, api=self.session) for r in resp]

    def get_presigned_url(self, instance, format='parquet'):
        uri = self._uri('/organizations/{orgId}/datasets/{datasetId}/views/instances/{graphViewInstanceId}/url?format={format}',
                        format=format, **self._kwargs(instance.view.dataset, instance=instance))
        return self._get(uri)
