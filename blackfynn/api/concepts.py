# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from future.utils import string_types

import itertools
import json

import requests

from blackfynn.api.base import APIBase
from blackfynn.models import (
    DataPackage,
    LinkedModelProperty,
    LinkedModelValue,
    Model,
    ModelFilter,
    ModelJoin,
    ModelProperty,
    ModelSelect,
    ModelTemplate,
    ProxyInstance,
    QueryResult,
    Record,
    RecordSet,
    Relationship,
    RelationshipProperty,
    RelationshipSet,
    RelationshipType,
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ModelsAPIBase(APIBase):
    def _get_concept_type(self, concept, instance=None):
        if isinstance(concept, Model):
            return concept.type
        elif isinstance(concept, string_types):
            return concept
        elif isinstance(instance, Record):
            return instance.type
        else:
            raise Exception(
                "could not get concept type from concept {} or instance {} ".format(
                    concept, instance
                )
            )

    def _get_relationship_type(self, relationship, instance=None):
        if isinstance(relationship, RelationshipType):
            return relationship.type
        elif isinstance(relationship, string_types):
            return relationship
        elif isinstance(instance, Relationship):
            return instance.type
        else:
            raise Exception(
                "could not get relationship type from relationship {} or instance {} ".format(
                    relationship, instance
                )
            )


class ModelsAPI(ModelsAPIBase):
    name = "concepts"

    def __init__(self, session):
        self.host = (
            session._host
            if session._model_service_host == None
            else session._model_service_host
        )
        self.base_uri = (
            "/models/datasets" if session._model_service_host == None else "/datasets"
        )
        self.instances = RecordsAPI(session)
        self.relationships = ModelRelationshipsAPI(session)
        self.proxies = ModelProxiesAPI(session)
        self.query = ModelQueryAPI(session)
        super(ModelsAPI, self).__init__(session)

    def get_properties(self, dataset, concept):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        resp = self._get(
            self._uri(
                "/{dataset_id}/concepts/{id}/properties",
                dataset_id=dataset_id,
                id=concept_id,
            )
        )
        return [ModelProperty.from_dict(r) for r in resp]

    def get_linked_properties(self, dataset, concept):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        resp = self._get(
            self._uri(
                "/{dataset_id}/concepts/{id}/linked",
                dataset_id=dataset_id,
                id=concept_id,
            )
        )
        return {r["link"]["name"]: LinkedModelProperty.from_dict(r) for r in resp}

    def update_properties(self, dataset, concept):
        assert isinstance(concept, Model), "concept must be type Model"
        assert concept.schema, "concept schema cannot be empty"
        data = concept.as_dict()["schema"]
        dataset_id = self._get_id(dataset)
        resp = self._put(
            self._uri(
                "/{dataset_id}/concepts/{id}/properties",
                dataset_id=dataset_id,
                id=concept.id,
            ),
            json=data,
        )
        return [ModelProperty.from_dict(r) for r in resp]

    def update_linked_property(self, dataset, concept, prop):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        prop_id = self._get_id(prop)
        resp = self._put(
            self._uri(
                "/{dataset_id}/concepts/{id}/linked/{prop_id}",
                dataset_id=dataset_id,
                id=concept_id,
                prop_id=prop_id,
            ),
            json=prop.as_dict(),
        )
        return LinkedModelProperty.from_dict(resp)

    def delete_property(self, dataset, concept, prop):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        property_id = self._get_id(prop)
        return self._del(
            self._uri(
                "/{dataset_id}/concepts/{concept_id}/properties/{property_id}",
                dataset_id=dataset_id,
                concept_id=concept_id,
                property_id=property_id,
            )
        )

    def delete_linked_property(self, dataset, concept, prop):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        prop_id = self._get_id(prop)
        self._del(
            self._uri(
                "/{dataset_id}/concepts/{id}/linked/{prop_id}",
                dataset_id=dataset_id,
                id=concept_id,
                prop_id=prop_id,
            )
        )

    def get(self, dataset, concept):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        r = self._get(
            self._uri(
                "/{dataset_id}/concepts/{id}", dataset_id=dataset_id, id=concept_id
            )
        )
        r["dataset_id"] = r.get("dataset_id", dataset_id)
        r["schema"] = self.get_properties(dataset, concept)
        r["linked"] = self.get_linked_properties(dataset, concept)
        return Model.from_dict(r, api=self.session)

    def delete(self, dataset, concept):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        return self._del(
            self._uri(
                "/{dataset_id}/concepts/{id}", dataset_id=dataset_id, id=concept.id
            )
        )

    def update(self, dataset, concept):
        assert isinstance(concept, Model), "concept must be type Model"
        data = concept.as_dict()
        data["id"] = concept.id
        dataset_id = self._get_id(dataset)
        r = self._put(
            self._uri(
                "/{dataset_id}/concepts/{id}", dataset_id=dataset_id, id=concept.id
            ),
            json=data,
        )
        r["dataset_id"] = r.get("dataset_id", dataset_id)
        if concept.schema:
            r["schema"] = self.update_properties(dataset, concept)
        if concept.linked:
            r["linked"] = {
                name: self.update_linked_property(dataset, concept, link)
                for name, link in concept.linked.items()
            }
        updated = Model.from_dict(r, api=self.session)
        return updated

    def create(self, dataset, concept):
        assert isinstance(concept, Model), "concept must be type Model"
        dataset_id = self._get_id(dataset)
        r = self._post(
            self._uri("/{dataset_id}/concepts", dataset_id=dataset_id),
            json=concept.as_dict(),
        )
        concept.id = r["id"]
        r["dataset_id"] = r.get("dataset_id", dataset_id)

        if concept.schema:
            try:
                r["schema"] = self.update_properties(dataset, concept)
            except requests.exceptions.HTTPError as e:

                # If properties can not be created, roll back model creation so
                # the user can try again.
                self.delete(dataset, concept)

                raise Exception(
                    "Could not create model properties: {}".format(
                        e.response.json().get("detail", e.response.json())
                    )
                )

        return Model.from_dict(r, api=self.session)

    def create_linked_property(self, dataset, concept, prop):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        assert prop.name not in self.get_linked_properties(
            dataset, concept
        ), "Linked property '{}' already exists".format(prop.name)
        resp = self._post(
            self._uri(
                "/{dataset_id}/concepts/{id}/linked",
                dataset_id=dataset_id,
                id=concept_id,
            ),
            json=prop.as_dict(),
        )
        return LinkedModelProperty.from_dict(resp)

    def create_linked_properties(self, dataset, concept, props):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        for p in props:
            assert p.name not in self.get_linked_properties(
                dataset, concept
            ), "Linked property '{}' already exists".format(p.name)
        resp = self._post(
            self._uri(
                "/{dataset_id}/concepts/{id}/linked/bulk",
                dataset_id=dataset_id,
                id=concept_id,
            ),
            json=[p.as_dict() for p in props],
        )
        return [LinkedModelProperty.from_dict(r) for r in resp]

    def get_all(self, dataset):
        dataset_id = self._get_id(dataset)
        resp = self._get(
            self._uri("/{dataset_id}/concepts", dataset_id=dataset_id), stream=True
        )
        for r in resp:
            r["dataset_id"] = r.get("dataset_id", dataset_id)
            r["schema"] = self.get_properties(dataset, r["id"])
            r["linked"] = self.get_linked_properties(dataset, r["id"])
        concepts = [Model.from_dict(r, api=self.session) for r in resp]
        # for concept in concepts:
        #     concept.linked = {x.name: x for x in self.get_linked_properties(dataset, concept)}
        return {c.type: c for c in concepts}

    def delete_instances(self, dataset, concept, *instances):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        ids = [self._get_id(instance) for instance in instances]

        return self._del(
            self._uri(
                "/{dataset_id}/concepts/{id}/instances",
                dataset_id=dataset_id,
                id=concept_id,
            ),
            json=ids,
        )

    def files(self, dataset, concept, instance):
        """
        Return list of files (i.e. packages) related to record.
        """
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        instance_id = self._get_id(instance)
        resp = self._get(
            self._uri(
                "/{dataset_id}/concepts/{concept_id}/instances/{instance_id}/files",
                dataset_id=dataset_id,
                concept_id=concept_id,
                instance_id=instance_id,
            )
        )
        return [DataPackage.from_dict(pkg, api=self.session) for r, pkg in resp]

    def get_connected(self, dataset, model):
        """ Return a list of concepts related to the given model """
        dataset_id = self._get_id(dataset)
        model_id = self._get_id(model)
        resp = self._get(
            self._uri(
                "/{dataset_id}/concepts/{model_id}/related",
                dataset_id=dataset_id,
                model_id=model_id,
            ),
            stream=True,
        )
        for r in resp:
            r["dataset_id"] = r.get("dataset_id", dataset_id)
            r["schema"] = self.get_properties(dataset, r["id"])
            r["linked"] = self.get_linked_properties(dataset, r["id"])

        concepts = [Model.from_dict(r, api=self.session) for r in resp]
        return {c.type: c for c in concepts}

    def get_related(self, dataset, concept):
        """ Return all SchemaRelationships and the Concepts they point to """
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        resp = self._get(
            self._uri(
                "/{dataset_id}/concepts/{concept_id}/topology",
                dataset_id=dataset_id,
                concept_id=concept_id,
            )
        )
        for r in resp:
            r["dataset_id"] = r.get("dataset_id", dataset_id)
            r["schema"] = self.get_properties(dataset, r["id"])
            r["linked"] = self.get_linked_properties(dataset, r["id"])
        concepts = [Model.from_dict(r, api=self.session) for r in resp]
        return concepts

    def get_topology(self, dataset):
        dataset_id = self._get_id(dataset)
        resp = self._get(
            self._uri("/{dataset_id}/concepts/schema/graph", dataset_id=dataset_id)
        )
        # What is returned is a list mixing
        results = {"models": [], "relationships": [], "linked_properties": []}
        for r in resp:
            r["dataset_id"] = r.get("dataset_id", dataset_id)
            if r.get("type") == "schemaRelationship":
                # This is a relationship
                results["relationships"].append(
                    Relationship.from_dict(r, api=self.session)
                )
            elif r.get("type") == "schemaLinkedProperty":
                # This is a linked property type
                results["linked_properties"].append(LinkedModelProperty.from_dict(r))
            else:
                # This is a model
                r["schema"] = self.get_properties(dataset, r["id"])
                r["linked"] = self.get_linked_properties(dataset, r["id"])
                results["models"].append(Model.from_dict(r, api=self.session))
        return results

    def get_summary(self, dataset):
        dataset_id = self._get_id(dataset)
        resp = self._get(
            self._uri("/{dataset_id}/concepts/graph/summary", dataset_id=dataset_id)
        )
        return resp


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Model Instances
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class RecordsAPI(ModelsAPIBase):
    name = "concepts.instances"

    def __init__(self, session):
        if session._model_service_host != None:
            self.host = session._model_service_host
        self.base_uri = (
            "/models/datasets" if session._model_service_host == None else "/datasets"
        )
        super(RecordsAPI, self).__init__(session)

    def get(self, dataset, instance, concept=None):
        dataset_id = self._get_id(dataset)
        instance_id = self._get_id(instance)
        concept_type = self._get_concept_type(concept, instance)

        r = self._get(
            self._uri(
                "/{dataset_id}/concepts/{concept_type}/instances/{id}",
                dataset_id=dataset_id,
                concept_type=concept_type,
                id=instance_id,
            )
        )
        r["dataset_id"] = r.get("dataset_id", dataset_id)
        return Record.from_dict(r, api=self.session)

    def relations(self, dataset, instance, related_concept, concept=None):
        dataset_id = self._get_id(dataset)
        instance_id = self._get_id(instance)
        related_concept_type = self._get_id(related_concept)
        concept_type = self._get_concept_type(concept, instance)

        res = self._get(
            self._uri(
                "/{dataset_id}/concepts/{concept_type}/instances/{id}/relations/{related_concept_type}",
                dataset_id=dataset_id,
                concept_type=concept_type,
                id=instance_id,
                related_concept_type=related_concept_type,
            )
        )

        relations = []
        for r in res:
            relationship = r[0]
            concept = r[1]

            relationship["dataset_id"] = relationship.get("dataset_id", dataset_id)
            concept["dataset_id"] = concept.get("dataset_id", dataset_id)

            relationship = Relationship.from_dict(relationship, api=self.session)
            concept = Record.from_dict(concept, api=self.session)

            relations.append((relationship, concept))

        return relations

    def get_all(self, dataset, concept, limit=100, offset=0):
        dataset_id = self._get_id(dataset)
        concept_type = self._get_concept_type(concept)

        resp = self._get(
            self._uri(
                "/{dataset_id}/concepts/{concept_type}/instances",
                dataset_id=dataset_id,
                concept_type=concept_type,
            ),
            params=dict(limit=limit, offset=offset),
            stream=True,
        )
        for r in resp:
            r["dataset_id"] = r.get("dataset_id", dataset_id)
        instances = [Record.from_dict(r, api=self.session) for r in resp]

        return RecordSet(concept, instances)

    def delete(self, dataset, instance):
        assert isinstance(instance, Record), "instance must be type Record"
        dataset_id = self._get_id(dataset)
        return self._del(
            self._uri(
                "/{dataset_id}/concepts/{concept_type}/instances/{id}",
                dataset_id=dataset_id,
                concept_type=instance.type,
                id=instance.id,
            )
        )

    def create(self, dataset, instance):
        assert isinstance(instance, Record), "instance must be type Record"
        dataset_id = self._get_id(dataset)
        r = self._post(
            self._uri(
                "/{dataset_id}/concepts/{concept_type}/instances",
                dataset_id=dataset_id,
                concept_type=instance.type,
            ),
            json=instance.as_dict(),
        )
        r["dataset_id"] = r.get("dataset_id", dataset_id)
        return Record.from_dict(r, api=self.session)

    def update(self, dataset, instance):
        assert isinstance(instance, Record), "instance must be type Record"
        dataset_id = self._get_id(dataset)
        r = self._put(
            self._uri(
                "/{dataset_id}/concepts/{concept_type}/instances/{id}",
                dataset_id=dataset_id,
                concept_type=instance.type,
                id=instance.id,
            ),
            json=instance.as_dict(),
        )
        r["dataset_id"] = r.get("dataset_id", dataset_id)
        return Record.from_dict(r, api=self.session)

    def create_many(self, dataset, concept, *instances):
        instance_type = instances[0].type
        for inst in instances:
            assert isinstance(inst, Record), "instance must be type Record"
            assert (
                inst.type == instance_type
            ), "Expected instance of type {}, found instance of type {}".format(
                instance_type, inst.type
            )
        dataset_id = self._get_id(dataset)
        values = [inst.as_dict() for inst in instances]
        resp = self._post(
            self._uri(
                "/{dataset_id}/concepts/{concept_type}/instances/batch",
                dataset_id=dataset_id,
                concept_type=instance_type,
            ),
            json=values,
            stream=True,
        )

        for r in resp:
            r["dataset_id"] = r.get("dataset_id", dataset_id)
        instances = [Record.from_dict(r, api=self.session) for r in resp]
        return RecordSet(concept, instances)

    def get_all_related(self, dataset, source_instance):
        related = self.get_counts(dataset, source_instance)
        return {
            item["name"]: self.get_all_related_of_type(
                dataset, source_instance, item["name"]
            )
            for item in related
            if not (item["name"] == "package" and item["displayName"] == "Files")
            # ^^ TODO: have API provide better means of distinguishing proxy vs. model
        }

    def get_all_related_of_type(
        self, dataset, source_instance, return_type, source_concept=None
    ):
        """
        Return all records of type return_type related to instance.
        """
        dataset_id = self._get_id(dataset)
        instance_id = self._get_id(source_instance)
        instance_type = self._get_concept_type(source_concept, source_instance)

        resp = []
        limit = 100
        for offset in itertools.count(0, limit):
            batch = self._get(
                self._uri(
                    "/{dataset_id}/concepts/{instance_type}/instances/{instance_id}/relations/{return_type}",
                    dataset_id=dataset_id,
                    instance_type=instance_type,
                    instance_id=instance_id,
                    return_type=return_type,
                ),
                params={"limit": limit, "offset": offset},
            )

            if not batch:
                break

            resp += batch

        for edge, node in resp:
            node["dataset_id"] = node.get("dataset_id", dataset_id)
        if not isinstance(return_type, Model):
            return_type = self.session.concepts.get(dataset, return_type)
        records = [Record.from_dict(r, api=self.session) for _, r in resp]
        return RecordSet(return_type, records)

    def get_counts(self, dataset, instance, concept=None):
        dataset_id = self._get_id(dataset)
        concept_type = self._get_concept_type(concept, instance)
        instance_id = self._get_id(instance)
        return self._get(
            self._uri(
                "/{dataset_id}/concepts/{concept_type}/instances/{instance_id}/relationCounts",
                dataset_id=dataset_id,
                concept_type=concept_type,
                instance_id=instance_id,
            )
        )

    def get_linked_values(self, dataset, concept, instance):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        instance_id = self._get_id(instance)
        resp = self._get(
            self._uri(
                "/{dataset_id}/concepts/{id}/instances/{instance_id}/linked",
                dataset_id=dataset_id,
                id=concept_id,
                instance_id=instance_id,
            )
        )
        values = []
        for r in resp:
            link_type = concept.get_linked_property(r["schemaLinkedPropertyId"])
            target = concept._api.concepts.get(dataset, link_type.target)
            values.append(
                LinkedModelValue.from_dict(
                    r, source_model=concept, target_model=target, link_type=link_type
                )
            )
        return values

    def create_link(self, dataset, concept, instance, payload):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        instance_id = self._get_id(instance)

        # Delete any existing links of the given type:
        for link in self.get_linked_values(dataset, concept, instance):
            if link.type.id == payload["schemaLinkedPropertyId"]:
                self.remove_link(dataset, concept, instance, link)

        resp = self._post(
            self._uri(
                "/{dataset_id}/concepts/{id}/instances/{instance_id}/linked",
                dataset_id=dataset_id,
                id=concept_id,
                instance_id=instance_id,
            ),
            json=payload,
        )
        link_type = concept.get_linked_property(resp["schemaLinkedPropertyId"])
        target = concept._api.concepts.get(dataset, link_type.target)
        return LinkedModelValue.from_dict(
            resp, source_model=concept, target_model=target, link_type=link_type
        )

    def create_link_batch(self, dataset, concept, instance, payload):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        instance_id = self._get_id(instance)

        json = {"data": payload}

        resp = self._post(
            self._uri(
                "/{dataset_id}/concepts/{concept_id}/instances/{instance_id}/linked/batch",
                dataset_id=dataset_id,
                concept_id=concept_id,
                instance_id=instance_id,
            ),
            json=json,
        )

        results = resp["data"]

        return results
        # TODO: LinkedModelValue requires a fully instantiated target model
        # it's quite inefficient to retrieve individual models in a loop via `concepts.get`,
        # but we don't have a better way to retrieve them at this time.
        # For the sake of speed, we just return the raw JSON for now
        # linked_model_values = []
        # for r in results:
        #     link_type = concept.get_linked_property(r["schemaLinkedPropertyId"])
        #     target = concept._api.concepts.get(dataset, link_type.target)
        #     linked_model_values.append(
        #         LinkedModelValue.from_dict(
        #             r,
        #             source_model=concept,
        #             target_model=target,
        #             link_type=link_type
        #         )
        #     )
        # return linked_model_values

    def remove_link(self, dataset, concept, instance, value):
        dataset_id = self._get_id(dataset)
        concept_id = self._get_id(concept)
        instance_id = self._get_id(instance)
        link_id = self._get_id(value)
        self._del(
            self._uri(
                "/{dataset_id}/concepts/{id}/instances/{instance_id}/linked/{link_id}",
                dataset_id=dataset_id,
                id=concept_id,
                instance_id=instance_id,
                link_id=link_id,
            )
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Relationships
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ModelRelationshipsAPI(ModelsAPIBase):
    name = "concepts.relationships"

    def __init__(self, session):
        if session._model_service_host != None:
            self.host = session._model_service_host
        self.base_uri = (
            "/models/datasets" if session._model_service_host == None else "/datasets"
        )
        self.instances = ModelRelationshipInstancesAPI(session)
        super(ModelRelationshipsAPI, self).__init__(session)

    def create(self, dataset, relationship):
        assert isinstance(
            relationship, RelationshipType
        ), "Must be of type Relationship"
        dataset_id = self._get_id(dataset)
        rel_dict = relationship.as_dict()
        r = self._post(
            self._uri("/{dataset_id}/relationships", dataset_id=dataset_id),
            json=rel_dict,
        )
        r["dataset_id"] = r.get("dataset_id", dataset_id)
        return RelationshipType.from_dict(r, api=self.session)

    def get(self, dataset, relationship):
        dataset_id = self._get_id(dataset)
        relationship_id = self._get_id(relationship)
        r = self._get(
            self._uri(
                "/{dataset_id}/relationships/{r_id}",
                dataset_id=dataset_id,
                r_id=relationship_id,
            )
        )
        r["dataset_id"] = r.get("dataset_id", dataset_id)
        return RelationshipType.from_dict(r, api=self.session)

    def get_all(self, dataset):
        dataset_id = self._get_id(dataset)
        resp = self._get(
            self._uri("/{dataset_id}/relationships", dataset_id=dataset_id), stream=True
        )
        for r in resp:
            r["dataset_id"] = r.get("dataset_id", dataset_id)
        relations = [RelationshipType.from_dict(r, api=self.session) for r in resp]
        return {r.type: r for r in relations}


class ModelRelationshipInstancesAPI(ModelsAPIBase):
    name = "concepts.relationships.instances"

    def __init__(self, session):
        if session._model_service_host != None:
            self.host = session._model_service_host
        self.base_uri = (
            "/models/datasets" if session._model_service_host == None else "/datasets"
        )
        super(ModelRelationshipInstancesAPI, self).__init__(session)

    def get_all(self, dataset, relationship):
        dataset_id = self._get_id(dataset)
        relationship_id = self._get_id(relationship)

        resp = self._get(
            self._uri(
                "/{dataset_id}/relationships/{r_id}/instances",
                dataset_id=dataset_id,
                r_id=relationship_id,
            ),
            stream=True,
        )
        for r in resp:
            r["dataset_id"] = r.get("dataset_id", dataset_id)
        instances = [Relationship.from_dict(r, api=self.session) for r in resp]
        return RelationshipSet(relationship, instances)

    def get(self, dataset, instance, relationship=None):
        dataset_id = self._get_id(dataset)
        instance_id = self._get_id(instance)
        relationship_type = self._get_relationship_type(relationship, instance)
        r = self._get(
            self._uri(
                "/{dataset_id}/relationships/{r_type}/instances/{id}",
                dataset_id=dataset_id,
                r_type=relationship_type,
                id=instance_id,
            )
        )
        r["dataset_id"] = r.get("dataset_id", dataset_id)
        return Relationship.from_dict(r, api=self.session)

    def delete(self, dataset, instance):
        assert isinstance(
            instance, Relationship
        ), "instance must be of type Relationship"
        dataset_id = self._get_id(dataset)
        return self._del(
            self._uri(
                "/{dataset_id}/relationships/{r_type}/instances/{id}",
                dataset_id=dataset_id,
                r_type=instance.type,
                id=instance.id,
            )
        )

    def link(self, dataset, relationship, source, destination, values=dict()):
        assert isinstance(
            source, (Record, DataPackage)
        ), "source must be an object of type Record or DataPackage"
        assert isinstance(
            destination, (Record, DataPackage)
        ), "destination must be an object of type Record or DataPackage"

        if isinstance(source, DataPackage):
            assert isinstance(
                destination, Record
            ), "DataPackages can only be linked to Records"
            return self.session.concepts.proxies.create(
                dataset,
                source.id,
                relationship,
                destination,
                values,
                "ToTarget",
                "package",
            )
        elif isinstance(destination, DataPackage):
            assert isinstance(
                source, Record
            ), "DataPackages can only be linked to Records"
            return self.session.concepts.proxies.create(
                dataset,
                destination.id,
                relationship,
                source,
                values,
                "FromTarget",
                "package",
            )
        else:
            dataset_id = self._get_id(dataset)
            relationship_type = self._get_relationship_type(relationship)
            values = [dict(name=k, value=v) for k, v in values.items()]
            instance = Relationship(
                dataset_id=dataset_id,
                type=relationship_type,
                source=source,
                destination=destination,
                values=values,
            )
            return self.create(dataset, instance)

    def create(self, dataset, instance):
        assert isinstance(
            instance, Relationship
        ), "instance must be of type Relationship"
        dataset_id = self._get_id(dataset)
        resp = self._post(
            self._uri(
                "/{dataset_id}/relationships/{r_type}/instances",
                dataset_id=dataset_id,
                r_type=instance.type,
            ),
            json=instance.as_dict(),
        )
        r = resp[0]  # responds with list
        r["dataset_id"] = r.get("dataset_id", dataset_id)
        return Relationship.from_dict(r, api=self.session)

    def create_many(self, dataset, relationship, *instances):
        assert all(
            [isinstance(i, Relationship) for i in instances]
        ), "instances must be of type Relationship"
        instance_type = instances[0].type
        dataset_id = self._get_id(dataset)
        values = [inst.as_dict() for inst in instances]
        resp = self._post(
            self._uri(
                "/{dataset_id}/relationships/{r_type}/instances/batch",
                dataset_id=dataset_id,
                r_type=instance_type,
            ),
            json=values,
        )

        for r in resp:
            r[0]["dataset_id"] = r[0].get("dataset_id", dataset_id)
        instances = [Relationship.from_dict(r[0], api=self.session) for r in resp]
        return RelationshipSet(relationship, instances)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Model Proxies
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ModelProxiesAPI(ModelsAPIBase):
    name = "concepts.proxies"

    proxy_types = ["package"]
    direction_types = ["FromTarget", "ToTarget"]

    def __init__(self, session):
        if session._model_service_host != None:
            self.host = session._model_service_host
        self.base_uri = (
            "/models/datasets" if session._model_service_host == None else "/datasets"
        )
        super(ModelProxiesAPI, self).__init__(session)

    def create(
        self,
        dataset,
        external_id,
        relationship,
        concept_instance,
        values,
        direction="ToTarget",
        proxy_type="package",
        concept=None,
    ):
        assert proxy_type in self.proxy_types, "proxy_type must be one of {}".format(
            self.proxy_types
        )
        assert direction in self.direction_types, "direction must be one of {}".format(
            self.direction_types
        )

        dataset_id = self._get_id(dataset)
        concept_instance_id = self._get_id(concept_instance)
        concept_type = self._get_concept_type(concept, concept_instance)
        relationship_type = self._get_relationship_type(relationship)
        relationshipData = [dict(name=k, value=v) for k, v in values.items()]

        request = {}
        request["externalId"] = external_id
        request["conceptType"] = concept_type
        request["conceptInstanceId"] = concept_instance_id
        request["targets"] = [
            {
                "direction": direction,
                "linkTarget": {"ConceptInstance": {"id": concept_instance_id}},
                "relationshipType": relationship_type,
                "relationshipData": relationshipData,
            }
        ]

        r = self._post(
            self._uri(
                "/{dataset_id}/proxy/{p_type}/instances",
                dataset_id=dataset_id,
                p_type=proxy_type,
            ),
            json=request,
        )
        instance = r[0]["relationshipInstance"]
        instance["dataset_id"] = instance.get("dataset_id", dataset_id)
        return Relationship.from_dict(instance, api=self.session)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Model Query
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ModelQuery(object):
    allowed_operators = set(["eq", "neq", "lt", "lte", "gt", "gte"])

    def __init__(self, query_api, model, dataset_id):
        self.query_api = query_api
        self.model = model
        self.dataset_id = dataset_id
        self._select = None
        self._filters = []
        self._joins = []
        self._offset = 0
        self._limit = 50

    def select(self, *join_keys):
        """
        Add a select clause to the query.

        Args:
            join_keys: (List[str|model]) The names of the targets to select on.

        Examples::

            Review.query() \
                .filter("is_complete", "eq", False) \
                .join("reviewer", ("id", "eq", "12345")) \
                .select(reviewer")
                .run()
        """
        self._select = ModelSelect(*join_keys)
        return self

    def filter(self, key, operator, value):
        """
        Add a filter to the query.

        Args:
            key: (string) The name of the property to test.

            operator: (string) The predicate operator.

            value (any) The right hand of the predicate to match against.

        Returns:
            The current query object.

        Example::

            Review.query() \
                .filter("is_complete", "eq", False) \
                .run()
        """
        assert isinstance(key, str), "key must be a string"
        assert (
            operator in self.allowed_operators
        ), "not a valid predicate operator: {}".format(operator)
        self._filters.append(ModelFilter(key, operator, value))
        return self

    def join(self, target, *filters):
        """
        Add a join clause to the query.

        Args:
            target: (string|model) The model to join to via some relationship.

            filters: (*tuple) Filter conditions to apply to the join. Each
                tuple is expected to be a triple (key, operator, value), much
                like the constructor for `ModelFilter`.

        Returns:
            The current query object.

        Example::

            Review.query() \
                .filter("is_complete", "eq", False) \
                .join("reviewer", ("id", "eq", "12345")) \
                .select(reviewer")
                .run()
        """
        assert isinstance(target, (str, Model)), "target must be a string or a model"
        self._joins.append(ModelJoin(target, *filters))
        return self

    def offset(self, value):
        """
        Adds an offset to the query.

        Args:
            value (int) The offset value.

        Returns:
            The current query object.

        Example::

            Review.query() \
                .filter("is_complete", "eq", False) \
                .offset(100)
                .run()
        """
        self._offset = value
        return self

    def limit(self, value):
        """
        Adds an limit to the query.

        Args:
            value (int) The limit value.

        Returns:
            The current query object.

        Example::

            Review.query() \
                .filter("is_complete", "eq", False) \
                .limit(100)
                .run()
        """
        self._limit = value
        return self

    def _build_query(self):
        query = {
            "type": {"concept": {"type": self.model.type}},
            "filters": [f.as_dict() for f in self._filters],
            "joins": [j.as_dict() for j in self._joins],
            "offset": self._offset,
            "limit": self._limit,
            "orderBy": {"Ascending": {"field": "$createdAt"}},
        }
        if self._select is not None:
            query["select"] = self._select.as_dict()
        return query

    def run(self):
        """
        Run the constructed query.

        Returns:
            A list of matching Record instances.
        """
        resp = self.query_api._post(
            self.query_api._uri("/{dataset_id}/query/run", dataset_id=self.dataset_id),
            json=self._build_query(),
        )
        if resp is None:
            return []

        records = []
        for r in resp:
            # get the target first:
            target_value = r["targetValue"]
            target_value["dataset_id"] = self.dataset_id
            target = Record.from_dict(target_value, api=self.query_api.session)

            # then any attached records by join type:
            joined = {}
            if self._select is not None:
                for join_key in self._select.join_keys:
                    if join_key in r:
                        join_value = r[join_key]
                        join_value["dataset_id"] = self.dataset_id
                        joined[join_key] = Record.from_dict(
                            join_value, api=self.query_api.session
                        )

            records.append(QueryResult(self.dataset_id, target, joined))

        return records


class ModelQueryAPI(ModelsAPIBase):
    name = "concepts.query"

    def __init__(self, session):
        if session._model_service_host != None:
            self.host = session._model_service_host

        self.base_uri = (
            "/models/datasets" if session._model_service_host == None else "/datasets"
        )
        super(ModelQueryAPI, self).__init__(session)

    def new(self, model, dataset_id):
        """
        Construct a new query.

        Args:
            model: The model to use as the join target.

            dataset_id: The ID of the dataset the model is contained in.

        Returns:
            A list of records fulfilling the conditions of the query.

        Example::

            self.new(model, dataset_id) \
                .filter("is_completed", "eq", False) \
                .run()
        """
        return ModelQuery(self, model, dataset_id)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Model Templates
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ModelTemplatesAPI(APIBase):

    base_uri = "/model-schema"
    name = "templates"

    def get_all(self):
        org_id = self._get_int_id(self.session._context)
        resp = self._get(self._uri("/organizations/{orgId}/templates", orgId=org_id))
        return [ModelTemplate.from_dict(t) for t in resp]

    def get(self, template_id):
        org_id = self._get_int_id(self.session._context)
        resp = self._get(
            self._uri(
                "/organizations/{orgId}/templates/{templateId}",
                orgId=org_id,
                templateId=template_id,
            )
        )
        return ModelTemplate.from_dict(resp)

    def validate(self, template):
        assert isinstance(template, ModelTemplate), "template must be type Template"
        response = self._post(self._uri("/validate"), json=template.as_dict())
        if response == "":
            return True
        else:
            return response

    def create(self, template):
        assert isinstance(template, ModelTemplate), "template must be type Template"
        org_id = self._get_int_id(self.session._context)
        resp = self._post(
            self._uri("/organizations/{orgId}/templates", orgId=org_id),
            json=template.as_dict(),
        )
        return ModelTemplate.from_dict(resp)

    def apply(self, dataset, template):
        org_id = self._get_int_id(self.session._context)
        dataset_id = self._get_int_id(dataset)
        template_id = self._get_id(template)
        resp = self._post(
            self._uri(
                "/organizations/{orgId}/templates/{templateId}/datasets/{datasetId}",
                orgId=org_id,
                templateId=template_id,
                datasetId=dataset_id,
            )
        )
        return [ModelProperty.from_dict(t) for t in resp]

    def delete(self, template_id):
        org_id = self._get_int_id(self.session._context)
        return self._del(
            self._uri(
                "/organizations/{orgId}/templates/{templateId}",
                orgId=org_id,
                templateId=template_id,
            )
        )
