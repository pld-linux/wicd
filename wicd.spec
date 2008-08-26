# TODO: Needs review
# TODO: Fix daemon status and stop (wicd dead but subsys locked but daemon running)
Summary:	wired and wireless network manager
Summary(pl.UTF-8):	Zarządca sieci przewodowych i bezprzewodowych
Name:		wicd
Version:	1.5.1
Release:	5
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/wicd/%{name}-%{version}.tar.gz
# Source0-md5:	dda372b0778de24552850d3d877d1b65
URL:		http://wicd.net/
# /etc/pld-release used to detect platform
BuildRequires:	issue
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	python-dbus
Requires:	python-pygobject
Requires:	python-pygtk-glade >= 2:2.0
Requires:	python-pygtk-gtk >= 2:2.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Wicd is an open source wired and wireless network manager for Linux
which aims to provide a simple interface to connect to networks with a
wide variety of settings.

%description -l pl.UTF-8
Wicd jest zarządcą sieci przewodowych i bezprzewodowych dla Linuksa,
mającym zapewnić prosty interfejs do podłączania do sieci z
różnorakimi opcjami.

%prep
%setup -q
%{__python} setup.py configure

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/wicd-client
%attr(755,root,root) %{_sbindir}/wicd
# NOTE: must be in /usr/lib even on 64bit systems
%{_prefix}/lib/%{name}
%attr(755,root,root) %{_prefix}/lib/%{name}/*.py
%dir %{py_sitescriptdir}/wicd
%{py_sitescriptdir}/wicd/*.py[co]
%{py_sitescriptdir}/Wicd-*.egg-info
%{_datadir}/%{name}
%{_datadir}/autostart/wicd-tray.desktop
%{_desktopdir}/wicd.desktop
%{_iconsdir}/hicolor/*/apps/wicd-client.*
%{_pixmapsdir}/%{name}
%{_sysconfdir}/wicd
%{_sysconfdir}/xdg/autostart/wicd-tray.desktop
/etc/dbus-1/system.d/wicd.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
/var/lib/%{name}
/var/log/%{name}
%{_mandir}/man5/wicd-manager-settings.conf.5*
%{_mandir}/man5/wicd-wired-settings.conf.5*
%{_mandir}/man5/wicd-wireless-settings.conf.5*
%{_mandir}/man8/wicd.8*
