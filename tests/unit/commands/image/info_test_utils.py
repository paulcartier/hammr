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

import pyxb
import datetime
from uforge.objects import uforge

def create_image(target_format_name):
    image_format = uforge.ImageFormat()
    image_format.name = target_format_name

    target_format = uforge.TargetFormat()
    target_format.name = target_format_name
    target_format.format = image_format

    image = uforge.Image()
    image.targetFormat = target_format
    return image

def create_image_do_info():
    image = create_image("aws")

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


def create_image_do_info_format_docker():
    image = create_image_do_info()
    image.targetFormat.name = "docker"
    image.targetFormat.format.name = "docker"
    image.registeringName = "registering name"
    image.entrypoint = "['/usr/sbin/httpd','-DFOREGROUND']"

    return image


def create_image_do_info_status_error():
    image = create_image_do_info()
    image.status.complete = False
    image.status.error = True
    image.status.errorMessage = "error message"

    return image


def create_appliance_do_info():
    appliance = uforge.Appliance()
    appliance.distributionName = "CentOS 7"
    appliance.archName = "x86_64"
    appliance.dbId = 104
    appliance.uri = "users/guest/appliances/104"
    appliance.description = "Description"

    return appliance


def create_scanned_instance_do_info():
    scanned_instance = uforge.ScannedInstance()
    scanned_instance.uri = "users/guest/scannedinstances/10"
    scanned_instance.dbId = 104
    distribution = uforge.Distribution()
    distribution.name = "CentOS"
    distribution.version = "7"
    distribution.arch = "x86_64"
    scanned_instance.distribution = distribution

    return scanned_instance


def create_my_software_do_info():
    my_software = uforge.MySoftware()
    my_software.uri = "users/guest/mysoftware/518"
    my_software.dbId = 10
    my_software.description = "description"

    return my_software


def create_container_template_do_info():
    container_template = uforge.ContainerTemplate()
    container_template.uri = "users/guest/mysoftware/518/templates/1"
    distribution = uforge.Distribution()
    distribution.name = "CentOS"
    distribution.version = "7"
    distribution.arch = "x86_64"
    container_template.distribution = distribution

    return container_template


def create_pimage_do_info():
    pimage = uforge.PublishImageAws()
    pimage.cloudId = "Cloud ID"
    pimage.imageUri = "users/14/appliances/102/images/1"
    pimage.targetFormat = uforge.targetFormat()
    pimage.targetFormat.dbId = 1234

    status = uforge.OpStatus()
    status.complete = True
    pimage.status = status

    return pimage


def create_images_do_info(image):
    images = uforge.Images()
    images.images = pyxb.BIND()
    images.images.append(image)

    return images


def create_pimages_do_info(pimage=None):
    pimages = uforge.publishImages()
    pimages.publishImages = pyxb.BIND()
    if pimage:
        pimages.publishImages.append(pimage)

    return pimages
