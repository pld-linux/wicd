Summary:	wired and wireless network manager
Summary(pl.UTF-8):	Zarządca sieci przewodowych i bezprzewodowych
Name:		wicd
Version:	1.6.2.2
Release:	3
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/wicd/%{name}-%{version}.tar.gz
# Source0-md5:	acbbe695abf7ff83161c62317dfc7509
Source1:	%{name}.init
Patch0:		%{name}-init_status.patch
URL:		http://www.wicd.net/
# /etc/pld-release used to detect platform
BuildRequires:	issue
BuildRequires:	libiw-devel
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	dbus(org.freedesktop.Notifications)
Requires:	python-dbus
Requires:	python-pygobject
Requires:	python-pygtk-glade >= 2:2.0
Requires:	python-pygtk-gtk >= 2:2.0
Obsoletes:	wicd < 1.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Wicd is an open source wired and wireless network manager for Linux
which aims to provide a simple interface to connect to networks with a
wide variety of settings.

%description -l pl.UTF-8
Wicd jest zarządcą sieci przewodowych i bezprzewodowych dla Linuksa,
mającym zapewnić prosty interfejs do podłączania do sieci z
różnorakimi opcjami.

%package client-curses
Summary:	wicd console client
Summary(pl.UTF-8):	klient wicd dla konsoli
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	python-urwid

%description client-curses
wicd curses client.

%description client-curses -l pl.UTF-8
Klient wicd dla konsoli.

%package -n pm-utils-wicd
Summary:	wicd script for pm-utils
Summary(pl.UTF-8):	Skrypt wicd dla pm-utils
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	pm-utils

%description -n pm-utils-wicd
wicd script for pm-utils.

%description -n pm-utils-wicd -l pl.UTF-8
Skrypt wicd dla pm-utils.

%prep
%setup -q
%patch0 -p1

mv translations/{ar_EG,ar}
mv translations/{de_DE,de}
mv translations/{es_ES,es}
mv translations/{it_IT,it}
mv translations/{nl_NL,nl}
mv translations/{no,nb}
mv translations/{ru_RU,ru}

%build
%{__python} setup.py configure \
	--backends %{_libdir}/%{name}/backends \
	--lib %{_libdir}/%{name} \
	--pidfile /var/run/wicd.pid \
	--pmutils %{_libdir}/pm-utils/sleep.d

%{__python} setup.py build

cd depends/python-iwscan
%{__python} setup.py build
cd ../python-wpactrl
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

cd depends/python-iwscan
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

cd ../python-wpactrl
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/wicd

cd ../..

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%find_lang %{name}

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

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
%doc AUTHORS CHANGES INSTALL README
%attr(755,root,root) %{_bindir}/wicd-client
%attr(755,root,root) %{_sbindir}/wicd
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man1/wicd-client.1*
%{_mandir}/man5/wicd-manager-settings.conf.5*
%{_mandir}/man5/wicd-wired-settings.conf.5*
%{_mandir}/man5/wicd-wireless-settings.conf.5*
%{_mandir}/man8/wicd.8*
/etc/dbus-1/system.d/wicd.conf
%{_sysconfdir}/wicd
%{_sysconfdir}/xdg/autostart/wicd-tray.desktop

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/backends
%attr(755,root,root) %{_libdir}/%{name}/*.py
%attr(755,root,root) %{_libdir}/%{name}/backends/*.py
%exclude %{_libdir}/%{name}/*curses*.py

%{_datadir}/%{name}
%{_datadir}/autostart/wicd-tray.desktop

%{_desktopdir}/wicd.desktop
%{_iconsdir}/hicolor/*/apps/wicd-client.*
%{_pixmapsdir}/%{name}

%dir %{py_sitescriptdir}/wicd
%{py_sitescriptdir}/wicd/*.py[co]
%{py_sitescriptdir}/Wicd-*.egg-info

%{py_sitedir}/iwscan.so
%{py_sitedir}/wpactrl.so

%if "%{py_ver}" > "2.4"
%{py_sitedir}/iwscan-*.egg-info
%{py_sitedir}/wpactrl-*.egg-info
%endif

%dir /var/lib/%{name}
/var/lib/%{name}/WHEREAREMYFILES

%dir /var/log/%{name}

%files client-curses
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wicd-curses
%attr(755,root,root) %{_libdir}/%{name}/*curses*.py
%{_mandir}/man8/wicd-curses.8*

%files -n pm-utils-wicd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pm-utils/sleep.d/*wicd
