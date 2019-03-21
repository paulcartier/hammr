# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 UShareSoft, All rights reserved
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from unittest import TestCase

import pyxb
from mock import patch, ANY, call
from uforge.application import Api
from uforge.objects import uforge

from hammr.commands.image import image
from texttable import Texttable

from hurry.filesize import size
from hammr.utils import constants
import datetime

class TestImage(TestCase):

    @patch('uforge.application.Api._Users._Images.Getall')
    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('texttable.Texttable.add_row')
    def test_do_list_check_size(self, mock_table_add_row, mock_api_pimg_getall, mock_api_getall):
        # given
        i = self.prepare_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")
        new_pimages = uforge.publishImages()
        new_pimages.publishImages = pyxb.BIND()
        mock_api_pimg_getall.return_value = new_pimages
        # when
        i.do_list("")

        # then
        self.assertEquals(mock_table_add_row.call_count, 1)
        mock_table_add_row.assert_called_with([ANY, ANY, ANY, ANY, ANY, ANY, size(6000), ANY, ANY])

    @patch('uforge.application.Api._Users._Images.Getall')
    @patch('hammr.commands.image.Image.do_info_draw_publication')
    @patch('hammr.commands.image.Image.do_info_draw_generation')
    @patch('hammr.commands.image.Image.do_info_draw_general')
    def test_do_info_should_call_draw_methods(self, mock_draw_general, mock_draw_generation, mock_draw_publication, mock_api_getall):
        # given
        i = self.prepare_image()
        info_image = self.create_image_do_info()

        mock_api_getall.return_value = self.create_images_do_info(info_image)

        # when
        i.do_info("--id 1")

        # then
        mock_draw_general.assert_called_once_with(info_image)
        mock_draw_generation.assert_called_once_with(info_image)
        mock_draw_publication.assert_called_once_with(info_image)

    @patch('hammr.commands.image.Image.do_info_draw_source')
    @patch('texttable.Texttable.add_row')
    @patch('texttable.Texttable.draw')
    def test_do_info_draw_general(self, mock_table_draw, mock_table_add_row, mock_draw_source):
        # given
        i = self.prepare_image()
        info_image = self.create_image_do_info()

        # when
        i.do_info_draw_general(info_image)

        # then
        calls = []
        calls.append(call(["Name", info_image.name]))
        calls.append(call(["Format", info_image.targetFormat.name]))
        calls.append(call(["Id", info_image.dbId]))
        calls.append(call(["Version", info_image.version]))
        calls.append(call(["Revision", info_image.revision]))
        calls.append(call(["Uri", info_image.uri]))
        calls.append(call(["Created", info_image.created.strftime("%Y-%m-%d %H:%M:%S")]))
        calls.append(call(["Size", size(info_image.fileSize)]))
        calls.append(call(["Compressed", "Yes" if info_image.compress else "No"]))

        mock_table_draw.assert_called_once()
        mock_draw_source.assert_called_once()
        self.assertEquals(mock_table_add_row.call_count, 9)
        mock_table_add_row.assert_has_calls(calls)

    @patch('hammr.commands.image.Image.do_info_draw_source')
    @patch('texttable.Texttable.add_row')
    @patch('texttable.Texttable.draw')
    def test_do_info_draw_general_docker_image(self, mock_table_draw, mock_table_add_row, mock_draw_source):
        # given
        i = self.prepare_image()
        info_image = self.create_image_do_info_format_docker()

        # when
        i.do_info_draw_general(info_image)

        # then
        calls = []
        calls.append(call(["Name", info_image.name]))
        calls.append(call(["Format", info_image.targetFormat.name]))
        calls.append(call(["Id", info_image.dbId]))
        calls.append(call(["Version", info_image.version]))
        calls.append(call(["Revision", info_image.revision]))
        calls.append(call(["Uri", info_image.uri]))
        calls.append(call(["Created", info_image.created.strftime("%Y-%m-%d %H:%M:%S")]))
        calls.append(call(["Size", size(info_image.fileSize)]))
        calls.append(call(["Compressed", "Yes" if info_image.compress else "No"]))
        calls.append(call(["RegisteringName", info_image.registeringName]))
        calls.append(call(["Entrypoint", info_image.entrypoint]))

        mock_table_draw.assert_called_once()
        mock_draw_source.assert_called_once()
        self.assertEquals(mock_table_add_row.call_count, 11)
        mock_table_add_row.assert_has_calls(calls)

    @patch('uforge.application.Api._Users._Appliances.Getall')
    @patch('texttable.Texttable.add_row')
    def test_do_info_draw_source_appliance(self, mock_table_add_row, mock_api_appliances_getall):
        # given
        i = self.prepare_image()
        appliance = self.create_appliance_do_info()

        mock_api_appliances_getall.return_value = self.create_appliances_do_info(appliance)

        # when
        i.do_info_draw_source(appliance.uri, Texttable(0))

        # then
        calls = []
        calls.append(call(["OS", appliance.distributionName + " " + appliance.archName]))
        calls.append(call(["Template Id", appliance.dbId]))
        calls.append(call(["Description", appliance.description]))

        self.assertEquals(mock_table_add_row.call_count, 3)
        mock_table_add_row.assert_has_calls(calls)

    @patch('uforge.application.Api._Users._Scannedinstances.Getall')
    @patch('uforge.application.Api._Users._Scans.Getall')
    @patch('uforge.application.Api._Users._Appliances.Getall')
    @patch('texttable.Texttable.add_row')
    def test_do_info_draw_source_scan(self, mock_table_add_row, mock_api_appliances_getall, mock_api_scans_getall, mock_api_scannedinstances_getall):
        # given
        i = self.prepare_image()
        scan = self.create_scan_do_info()
        scans = self.create_scans_do_info(scan)
        scanned_instance = self.create_scanned_instance_do_info()
        scanned_instances = uforge.ScannedInstances()
        scanned_instances.scannedInstances = pyxb.BIND()
        scanned_instances.scannedInstances.append(scanned_instance)

        mock_api_appliances_getall.return_value = self.create_appliances_do_info()
        mock_api_scans_getall.return_value = scans
        mock_api_scannedinstances_getall.return_value = scanned_instances

        # when
        i.do_info_draw_source(scan.uri, Texttable(0))

        # then
        calls = []
        distro = scanned_instance.distribution
        calls.append(call(["OS", distro.name + " " + distro.version + " " + distro.arch]))
        calls.append(call(["Scan Id", scanned_instance.dbId]))

        self.assertEquals(mock_table_add_row.call_count, 2)
        mock_table_add_row.assert_has_calls(calls)

    @patch('uforge.application.Api._Users._Mysoftware._Templates.Getall')
    @patch('uforge.application.Api._Users._Mysoftware.Getall')
    @patch('uforge.application.Api._Users._Scans.Getall')
    @patch('uforge.application.Api._Users._Appliances.Getall')
    @patch('texttable.Texttable.add_row')
    def test_do_info_draw_source_my_software(self, mock_table_add_row, mock_api_appliances_getall, mock_api_scans_getall, mock_api_mysoftware_getall,mock_api_templates_getall):
        # given
        i = self.prepare_image()
        my_software = self.create_my_software_do_info()
        container_template = self.create_container_template_do_info()
        my_software_list = uforge.MySoftwareList()
        my_software_list.mySoftwareList = pyxb.BIND()
        my_software_list.mySoftwareList.append(my_software)
        mock_api_mysoftware_getall.return_value = my_software_list
        container_templates = uforge.ContainerTemplates()
        container_templates.containerTemplates = pyxb.BIND()
        container_templates.containerTemplates.append(container_template)

        mock_api_appliances_getall.return_value = self.create_appliances_do_info()
        mock_api_scans_getall.return_value = self.create_scans_do_info()
        mock_api_templates_getall.return_value = container_templates

        # when
        i.do_info_draw_source(container_template.uri, Texttable(0))

        # then
        calls = []
        distro = container_template.distribution
        calls.append(call(["OS", distro.name + " " + distro.version + " " + distro.arch]))
        calls.append(call(["MySoftware Id", my_software.dbId]))
        calls.append(call(["Description", my_software.description]))

        self.assertEquals(mock_table_add_row.call_count, 3)
        mock_table_add_row.assert_has_calls(calls)

    @patch('texttable.Texttable.add_row')
    @patch('texttable.Texttable.draw')
    def test_do_info_draw_generation_without_error(self, mock_table_draw, mock_table_add_row):
        # given
        i = self.prepare_image()
        info_image = self.create_image_do_info()

        # when
        i.do_info_draw_generation(info_image)

        # then
        calls = []
        calls.append(call(["Status", "Done"]))
        calls.append(call(["Message", info_image.status.message]))

        self.assertEquals(mock_table_add_row.call_count, 2)
        mock_table_draw.assert_called_once()
        mock_table_add_row.assert_has_calls(calls)

    @patch('texttable.Texttable.add_row')
    @patch('texttable.Texttable.draw')
    def test_do_info_draw_generation_with_error(self, mock_table_draw, mock_table_add_row):
        # given
        i = self.prepare_image()
        info_image = self.create_image_do_info_status_error()

        # when
        i.do_info_draw_generation(info_image)

        # then
        calls = []
        calls.append(call(["Status", "Error"]))
        calls.append(call(["Error Message", info_image.status.message]))
        calls.append(call(["Detailed Error Message", info_image.status.errorMessage]))

        self.assertEquals(mock_table_add_row.call_count, 3)
        mock_table_draw.assert_called_once()
        mock_table_add_row.assert_has_calls(calls)

    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('texttable.Texttable.add_row')
    @patch('texttable.Texttable.draw')
    def test_do_info_draw_publication(self, mock_table_draw, mock_table_add_row, mock_api_pimg_getall):
        # given
        i = self.prepare_image()
        info_image = self.create_image_do_info()
        pimage = self.create_pimage_do_info()

        mock_api_pimg_getall.return_value = self.create_pimages_do_info(pimage)

        # when
        i.do_info_draw_publication(info_image)

        # then
        mock_table_draw.assert_called_once()
        mock_table_add_row.assert_called_once_with(["# Published", "Format Id : " + str(pimage.targetFormat.dbId) + " \nCloud Id : " + str(pimage.cloudId)])

    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('texttable.Texttable.add_row')
    @patch('texttable.Texttable.draw')
    def test_do_info_draw_publication_without_published_image(self, mock_table_draw, mock_table_add_row, mock_api_pimg_getall):
        # given
        i = self.prepare_image()
        info_image = self.create_image_do_info()
        pimage = self.create_pimages_do_info()

        mock_api_pimg_getall.return_value = pimage

        # when
        i.do_info_draw_publication(info_image)

        # then
        mock_table_draw.assert_called_once()
        mock_table_add_row.assert_called_once_with(["# Published", "No published images"])

    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_delete_return_2_for_wrong_image_uri(self, mock_api_getall, _raw_input):
        # Given
        i = self.prepare_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")

        # When
        return_value = i.do_delete("--id 1")

        # Then
        self.assertEqual(2, return_value)

    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_delete_return_2_for_wrong_arguments(self, mock_api_getall, _raw_input):
        # Given
        i = self.prepare_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")

        # When
        return_value = i.do_delete("--id 1 --test 18")

        # Then
        self.assertEqual(2, return_value)

    @patch('uforge.application.Api._Users._Appliances._Images.Delete')
    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_delete_return_0_when_ok(self, mock_api_getall, _raw_input, mock_api_delete):
        # Given
        i = self.prepare_image()
        mock_api_getall.return_value = self.create_images(6000, "users/14/appliances/102/images/1")

        # When
        return_value = i.do_delete("--id 1")

        # Then
        self.assertEqual(0, return_value)

    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_cancel_return_2_for_non_existing_image(self, mock_api_getall, _raw_input):
        # Given
        i = self.prepare_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")

        # When
        return_value = i.do_cancel("--id 14")

        # Then
        self.assertEqual(2, return_value)

    @patch("hammr.utils.publish_builders.publish_vcenter")
    def test_build_publish_image_return_the_publish_image_created(self, mock_publish_vcenter):
        # given
        i = self.prepare_image()

        builder = {
            "displayName": "vcenter-vm-name",
            "esxHost": "esxhost_vcenter",
            "datastore": "datastore_vcenter",
            "network": "network_vcenter"
        }

        cred_account = uforge.CredAccountVSphere()

        publish_image = uforge.PublishImageVSphere()
        publish_image.displayName = builder["displayName"]
        publish_image.esxHost = builder["esxHost"]
        publish_image.datastore = builder["datastore"]
        publish_image.network = builder["network"]

        mock_publish_vcenter.return_value = publish_image

        # when
        publish_image_retrieved = i.build_publish_image(self.create_image("vcenter"), builder, cred_account)

        # then
        mock_publish_vcenter.assert_called_with(builder, cred_account)
        self.assertEqual(publish_image_retrieved.displayName, builder["displayName"])
        self.assertEqual(publish_image_retrieved.esxHost, builder["esxHost"])
        self.assertEqual(publish_image_retrieved.datastore, builder["datastore"])
        self.assertEqual(publish_image_retrieved.network, builder["network"])

    def prepare_image(self):
        i = image.Image()
        i.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        i.login = "login"
        i.password = "password"

        return i

    def create_image(self, target_format_name):
        image_format = uforge.ImageFormat()
        image_format.name = target_format_name

        target_format = uforge.TargetFormat()
        target_format.name = target_format_name
        target_format.format = image_format

        image = uforge.Image()
        image.targetFormat = target_format
        return image

    def create_images(self, size, uri):
        new_images = uforge.Images()
        new_images.images = pyxb.BIND()

        new_image = self.create_image("vcenter")
        new_image.dbId = 1
        new_image.fileSize = size
        new_image.size = 0
        new_image.name = "test"
        new_image.status = "complete"
        new_image.created = datetime.datetime.now()
        new_image.compress = True
        new_image.uri = uri

        new_images.images.append(new_image)

        return new_images

    def create_image_do_info(self):
        image = self.create_image("aws")

        image.name = "test image"
        image.dbId = 1
        image.version = "1"
        image.revision = "2"
        image.uri = "users/14/appliances/102/images/1"
        image.fileSize = 1000
        image.compress = True
        image.created = datetime.datetime.now()

        status = uforge.OpStatus()
        status.message = "message"
        status.complete = True
        image.status = status

        return image

    def create_image_do_info_format_docker(self):
        image = self.create_image_do_info()
        image.targetFormat.name = "docker"
        image.targetFormat.format.name = "docker"
        image.registeringName = "registering name"
        image.entrypoint = "['\/usr\/sbin\/httpd','-DFOREGROUND']"

        return image

    def create_image_do_info_status_error(self):
        image = self.create_image_do_info()
        image.status.complete = False
        image.status.error = True
        image.status.errorMessage = "error message"

        return image

    def create_appliance_do_info(self):
        appliance = uforge.Appliance()
        appliance.distributionName = "CentOS 7"
        appliance.archName = "x86_64"
        appliance.dbId = 104
        appliance.uri = "users/guest/appliances/104"
        appliance.description = "Description"

        return appliance

    def create_scan_do_info(self):
        scannedinstance_uri = "users/guest/scannedinstances/10"

        scan = uforge.Scan()
        scan.uri = "users/guest/scannedinstances/10/scans/10"
        scan.scannedInstanceUri = scannedinstance_uri

        return scan

    def create_scanned_instance_do_info(self):
        scannedinstance_uri = "users/guest/scannedinstances/10"

        scanned_instance = uforge.ScannedInstance()
        scanned_instance.uri = scannedinstance_uri
        scanned_instance.dbId = 104
        distribution = uforge.Distribution()
        distribution.name = "CentOS"
        distribution.version = "7"
        distribution.arch = "x86_64"
        scanned_instance.distribution = distribution

        return scanned_instance

    def create_my_software_do_info(self):
        my_software = uforge.MySoftware()
        my_software.uri = "users/guest/mysoftware/518"
        my_software.dbId = 10
        my_software.description = "description"

        return my_software

    def create_container_template_do_info(self):
        container_template = uforge.ContainerTemplate()
        container_template.uri = "users/guest/mysoftware/518/templates/1"
        distribution = uforge.Distribution()
        distribution.name = "CentOS"
        distribution.version = "7"
        distribution.arch = "x86_64"
        container_template.distribution = distribution

        return container_template

    def create_pimage_do_info(self):
        pimage = uforge.PublishImageAws()
        pimage.cloudId = "Cloud ID"
        pimage.imageUri = "users/14/appliances/102/images/1"
        pimage.targetFormat = uforge.targetFormat()
        pimage.targetFormat.dbId = 1234

        return pimage

    def create_images_do_info(self, image):
        images = uforge.Images()
        images.images = pyxb.BIND()
        images.images.append(image)

        return images

    def create_appliances_do_info(self, appliance=None):
        appliances = uforge.Appliances()
        appliances.appliances = pyxb.BIND()
        if appliance:
            appliances.appliances.append(appliance)

        return appliances

    def create_scans_do_info(self, scan=None):
        scans = uforge.Scans()
        scans.scans = pyxb.BIND()
        if scan:
            scans.scans.append(scan)

        return scans

    def create_pimages_do_info(self, pimage=None):
        pimages = uforge.publishImages()
        pimages.publishImages = pyxb.BIND()
        if pimage:
            pimages.publishImages.append(pimage)

        return pimages