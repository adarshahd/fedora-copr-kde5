%global         framework kquickcharts

# uncomment to enable bootstrap mode
#global bootstrap 1

%if !0%{?bootstrap}
%global tests 1
%endif

Name:    kf5-%{framework}
Summary: A QtQuick module providing high-performance charts
Version: 5.67.0
Release: 1%{?dist}

# libs are LGPL, tools are GPL
# KDE e.V. may determine that future LGPL/GPL versions are accepted
License: LGPLv2+
URL:     https://cgit.kde.org/%{framework}.git

%global majmin %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{majmin}/%{framework}-%{version}.tar.xz

## upstreamable patches

## upstream patches

BuildRequires:  gcc-c++
BuildRequires:  extra-cmake-modules >= %{majmin}
BuildRequires:  cmake(Qt5Qml)
BuildRequires:  cmake(Qt5Quick)
BuildRequires:  cmake(Qt5QuickControls2)

%description
The Quick Charts module provides a set of charts that can be used from QtQuick
applications. They are intended to be used for both simple display of data as
well as continuous display of high-volume data (often referred to as plotters).
The charts use a system called distance fields for their accelerated rendering,
which provides ways of using the GPU for rendering 2D shapes without loss of
quality.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{framework}-%{version} -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. \
  -DBUILD_TESTING:BOOL=%{?tests:ON}%{!?tests:OFF}
popd

%make_build -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%check
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1
xvfb-run -a \
dbus-launch --exit-with-session \
time \
make test ARGS="--output-on-failure --timeout 300" -C %{_target_platform} ||:
%endif

%ldconfig_scriptlets

%files
%doc README.md
%license COPYING
%dir %{_kf5_qmldir}/org/kde/quickcharts
%{_kf5_qmldir}/org/kde/quickcharts/qmldir
%{_kf5_qmldir}/org/kde/quickcharts/*.so
%dir %{_kf5_qmldir}/org/kde/quickcharts/controls
%{_kf5_qmldir}/org/kde/quickcharts/controls/qmldir
%{_kf5_qmldir}/org/kde/quickcharts/controls/styles
%{_kf5_qmldir}/org/kde/quickcharts/controls/*.qml
%{_kf5_qmldir}/org/kde/quickcharts/controls/*.so

%files devel
%dir %{_kf5_libdir}/cmake/KF5QuickCharts
%{_kf5_libdir}/cmake/KF5QuickCharts/*.cmake

%changelog
* Tue Feb 11 2020 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.67.0-1
- 5.67.0

* Mon Jan 20 2020 Martin Kyral <martin.kyral@gmail.com> - 5.66.0-1
- 5.66.0