#!/usr/bin/env python
# Copyright (c) 2009, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Willow Garage, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author Tully Foote/tfoote@willowgarage.com

import subprocess

from ..installers import PackageManagerInstaller
from .source import SOURCE_INSTALLER

ALPINE_OS_NAME = 'alpine'
APK_INSTALLER = 'apk'

def register_installers(context):
    context.set_installer(APK_INSTALLER, ApkInstaller())

def register_platforms(context):
    context.add_os_installer_key(ALPINE_OS_NAME, SOURCE_INSTALLER)
    context.add_os_installer_key(ALPINE_OS_NAME, APK_INSTALLER)
    context.set_default_os_installer_key(ALPINE_OS_NAME, lambda self: APK_INSTALLER)

def apk_detect_single(p):
    return not subprocess.call(['apk', 'search', p], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def apk_detect(packages):
    return [p for p in packages if apk_detect_single(p)]

class ApkInstaller(PackageManagerInstaller):

    def __init__(self):
        super(ApkInstaller, self).__init__(apk_detect)

    def get_install_command(self, resolved, interactive=True, reinstall=False, quiet=False):
        packages = self.get_packages_to_install(resolved, reinstall=reinstall)
        if not packages:
            return []

        command  = ['apk', '-S']

        if not interactive:
            command.append('')
        if not reinstall:
            command.append('')
        if quiet:
            command.append('')

        return [self.elevate_priv(command + packages)]
