#!/bin/bash
sed -i -e "s#<platform>Red Hat Enterprise Linux 6</platform>#<platform>CentOS 6</platform>##g" /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-oval.xml
sed -i -e "s#cpe:/o:redhat:enterprise_linux:6#cpe:/o:centos:centos:6##g" /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-oval.xml
sed -i -e "s#cpe:/o:redhat:enterprise_linux#cpe:/o:centos:centos##g" /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml
