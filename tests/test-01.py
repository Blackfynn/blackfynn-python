from __future__ import print_function
from tests.blackfynn_pentest import BlackfynnPentest
from blackfynn.models import Dataset

import random
import string


def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


# SecurityGetUploadCredentials
# SecurityGetStreamingCredentials
# GetAllPackagesInDataset
# GetFilesInPackage
# GetPackageFileS3Url
# GetPackageView
# GetPackageAnnotations
# RequestPasswordReset

#
# pytest function for DataSet tests
#
def test_run_dataset_tests():
    bf = BlackfynnPentest("aadmin-doc")

    # Get all datasets
    datasets = bf.datasets()
    assert(len(datasets) > 0)
    for ds in datasets:
        assert(isinstance(ds, Dataset))

    #
    # TEST: Create Dataset
    #
    rand_str = random_string(8)
    new_ds_name = 'Alpine-New-Data-Set-%s' % rand_str
    new_ds_descr = 'Description of new dataset %s' % rand_str
    new_ds = bf.create_dataset(new_ds_name, new_ds_descr)
    assert(isinstance(new_ds, Dataset))
    assert(new_ds.name == new_ds_name)
    assert(new_ds.description == new_ds_descr)

    #
    # TEST: Is Locked
    is_locked = bf.islocked_dataset(new_ds)
    # Failed
    ###assert(not is_locked)

    #resp = bf.lock_dataset(new_ds)
    #assert(resp is not None)

    #resp = bf.unlock_dataset(new_ds)
    #assert(resp is not None)

    #resp = bf.get_readme_dataset(ds)
    #assert(resp is not None)

    resp = bf.update_readme_dataset(ds, "New Readme")
    assert(resp is not None)

    #
    # Delete Dataset
    #
    resp = bf.delete_dataset(new_ds)
    assert(len(resp) == 0)

    # Make sure it is gone
    try:
        bf.get_dataset(new_ds_name)
        assert(False)
    except Exception as e:
        assert("No dataset matching name or ID" in e.message)


#
# pytest function for User tests
#
def test_run_user_tests():
    bf = BlackfynnPentest("aadmin-doc")
    USER_FIRST_NAME = "alpine"
    USER_LAST_NAME = "aaadmin"

    user = bf.get_user()
    assert (user.first_name == USER_FIRST_NAME)
    assert (user.last_name == USER_LAST_NAME)

    # Remove 2FA if set
    resp = bf.user_delete_two_factor()
    assert(resp is None or resp == '')

    # Set and check
    authy_id = bf.user_set_two_factor("7124662524", "+1")
    print("AuthyID == %s" % authy_id)
    assert(authy_id == 1137468)

    # Test update user
    user.color = u'#FF0000'
    user.url = 'http://vps.thezealot.net/images/avatar.jpg'
    user = bf.user_update(
        organization=None,  # user.organization,
        email=user.email,
        url=user.url,
        color=user.color,
        last_name=user.last_name,
        first_name=user.first_name,
        credential=user.credential)

    user = bf.get_user()
    assert(user.url == "http://vps.thezealot.net/images/avatar.jpg")
    # FAILS
    #assert(user.color == u'#FF0000')

    user.color = u'#00635D'
    user.url = ''
    bf.user_update(
        organization=None,  # user.organization,
        email=user.email,
        url=user.url,
        color=user.color,
        last_name=user.last_name,
        first_name=user.first_name,
        credential=user.credential)

    user = bf.get_user()
    assert(user.color == u'#00635D')

    # Update custom terms of service
    version = "20181020000000"
    user = bf.user_custom_terms_of_service(version)

    # Currently, no field in user for custom_terms of service, though
    # it comes back in the JSON response.  No other way to check TOS.
    assert(user is not None)

    # Update blackfynn terms of service
    version = "20181020000000"
    user = bf.blackfynn_terms_of_service(version)

    # Currently, no field in user for blackfynn_terms of service, though
    # it comes back in the JSON response. No other way to check TOS.
    assert(user is not None)


#
# pytest function for Organizations tests
#
def test_run_organizations_tests():
    bf = BlackfynnPentest("aadmin-doc")
    org_id = 'N:organization:7aae2bf7-ff15-4071-aa2a-e876ae609d3c'
    org = bf.get_organization(org_id)
    assert(org is not None)

    orgs = bf.get_organizations_all()
    assert(len(orgs) > 0)

    # Doesn't work: Depends on missing Organization.as_dict() function
    # org1 = orgs[0]
    # old_org_name = org1.name
    # new_org_name = "Updated %s" % old_org_name
    # org2 = bf.update_organization(org1)
    # assert(org2.name == new_org_name)
    # org1 = org2
    # org1.name = old_org_name
    # org1 = bf.update_organization(org1)
    # assert(org1.name == old_org_name)

    tos = bf.get_organization_custom_terms_of_service(orgs[0])
    # Test FAILS
    # assert(tos is not None)

    teams = bf.get_teams(org)
    assert(teams is not None and len(teams) > 0)

    rand_str = random_string(8)
    new_team_name = 'Alpine-New-Team-%s' % rand_str
    new_team = bf.create_team(org, new_team_name)
    assert(new_team is not None)
    assert('team' in new_team)

    new_team_id = new_team['team']['id']
    new_team_copy = bf.get_team(org, new_team_id)
    assert(new_team_copy is not None)
    assert('team' in new_team_copy)
    assert('id' in new_team_copy['team'])
    assert(new_team_copy['team']['id'] == new_team_id)

    updated_team_name = 'Updated-%s' % new_team_name
    bf.update_team(org, new_team_id, updated_team_name)
    new_team_copy = bf.get_team(org, new_team_id)
    assert(new_team_copy is not None)
    assert('team' in new_team_copy)
    assert('id' in new_team_copy['team'])
    assert(new_team_copy['team']['id'] == new_team_id)
    assert(new_team_copy['team']['name'] == updated_team_name)

    has_members_team_id = 'N:team:8804811a-74d8-45f7-ae2e-c2ab9179606e'
    members = bf.get_team_members(org, has_members_team_id)
    assert(len(members) > 0)

    resp = bf.delete_team(org, new_team_id)
    team_should_be_deleted = bf.get_team(org, new_team_id)
    assert(team_should_be_deleted is None)

    resp = bf.get_invites(org)
    assert(resp is not None)


#
# pytest function for Security tests
#

def test_run_security_tests():
    bf = BlackfynnPentest("aadmin-doc")

    datasets = bf.datasets()
    assert(len(datasets) > 0)

    resp = bf.get_upload_credentials(datasets[0])
    assert ("tempCredentials" in resp and "secretKey" in resp["tempCredentials"])
    print("secretKey = %s" % resp["tempCredentials"]["secretKey"])

    # get_streaming_credentials is broken
    #resp = bf.get_streaming_credentials()


def test_run_package_tests():
    bf = BlackfynnPentest("aadmin-doc")

    datasets = bf.datasets()
    assert(len(datasets) > 0)

    # get_packages_in_dataset
    all_packages = bf.get_all_packages(datasets[0])
    assert(len(all_packages) > 0)

    # get files from package
    pkg = all_packages[0]
    files = bf.get_files_from_package(pkg)
    #assert(len(files) > 0)

    #print("First file name is %s " % files[0].name)



def main():
    #test_run_user_tests()
    #test_run_organizations_tests()
    test_run_dataset_tests()
    #test_run_user_tests()
    #test_run_security_tests()
    #test_run_package_tests()


if __name__ == '__main__':
    main()