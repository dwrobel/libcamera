%global forgeurl https://github.com/libcamera-org/libcamera
%global commit   b40a8d4b454008aeab4c0eb1f63a07083d7d7c74
%global date     20210728
%forgemeta

Name:    libcamera
Version: 0.0.0
Release: 0.4%{?snapshot:.%{snapshot}}%{?dist}
Summary: A library to support complex camera ISPs
# Libarary is LGPLv2.1+ and the cam tool is GPLv2
License: LGPLv2.1+ and GPLv2
URL:     http://libcamera.org/
Source0: %{forgesource}
# Reported as https://github.com/raspberrypi/linux/issues/4500
Patch0:  libcamera-Do-not-return-EINVAL-for-missing-recommended-ioctl.patch

BuildRequires: doxygen
BuildRequires: /usr/bin/git
BuildRequires: gcc-c++
BuildRequires: meson
BuildRequires: openssl
BuildRequires: ninja-build
BuildRequires: python3-jinja2
BuildRequires: python3-ply
BuildRequires: python3-pyyaml
BuildRequires: python3-sphinx
BuildRequires: boost-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: gnutls-devel
BuildRequires: libatomic
BuildRequires: libevent-devel
BuildRequires: libtiff-devel
BuildRequires: libudev-devel
BuildRequires: lttng-ust-devel
BuildRequires: systemd-devel
BuildRequires: pkgconfig(gtest)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(gstreamer-video-1.0)
BuildRequires: pkgconfig(gstreamer-allocators-1.0)

Requires:      qt5-qtbase-gui

%description
libcamera is a library that deals with heavy hardware image processing operations
of complex camera devices that are shared between the linux host all while allowing
offload of certain aspects to the control of complex camera hardware such as ISPs.

Hardware support includes USB UVC cameras, libv4l cameras as well as more complex
ISPs (Image Signal Processor).

%package     devel
Summary:     Development package for %{name}
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package     docs
Summary:     Documentation for %{name}
BuildArch:   noarch

%description docs
HTML based documentation for %{name} including getting started and API.

%package     ipa
Summary:     ISP Image Processing Algorithm Plugins for %{name}
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description ipa
Image Processing Algorithms plugins for interfacing with device
ISPs for %{name}

%package     tools
Summary:     Tools for %{name}
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description tools
Command line tools for %{name}

%package     qcam
Summary:     Graphical QCam application for %{name}
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description qcam
Graphical QCam application for %{name}

%package     gstreamer
Summary:     GSTreamer plugin to use %{name}
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description gstreamer
GSTreamer plugins for %{name}

%prep
%forgeautosetup -p1 -S git
# cam/qcam crash with LTO
%define _lto_cflags %{nil}
export CFLAGS="%{optflags} -Wno-deprecated-declarations"
export CXXFLAGS="%{optflags} -Wno-deprecated-declarations"

%meson -Dv4l2=true

%build
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%ldconfig_scriptlets ipa

%files
%license COPYING.rst LICENSES/
%{_libdir}/libcamera*.so
%{_libdir}/v4l2-compat.so

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-base.pc

%files docs
%doc %{_docdir}/%{name}-%{version}/

%files ipa
%{_datadir}/libcamera/
%{_libdir}/libcamera/
%{_libexecdir}/libcamera/

%files gstreamer
%{_libdir}/gstreamer-1.0/libgstlibcamera.so

%files qcam
%{_bindir}/qcam

%files tools
%{_bindir}/cam
%{_bindir}/lc-compliance

%changelog
* Mon Aug 02 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.0.0-0.4
- Add patch to not return EINVAL on unsupported ioctls on Raspberry Pi

* Fri Jul 30 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.0.0-0.3
- Update to the latest snapshot
- Switch to use forgemeta to easily fetch sources from github mirror

* Mon Apr 05 2021 Peter Robinson <pbrobinson@fedoraproject.org> 0.0.0-0.2.76a5861
- Update to snapshot 76a5861
- Enable gstreamer plugin and QCam tool
- More granular packaging

* Sat Jul 27 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.0.0-0.1.36d6229
- Initial package
