# TODO: Needs review
# TODO: Fix files list
# TODO: Fix daemon status and stop (wicd dead but subsys locked but daemon running)
%define 	module	wicd
Summary:	wired and wireless network manager
Summary(pl.UTF-8):	Zarządca sieci przewodowych i bezprzewodowych
Name:		wicd
Version:	1.5.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://master.dl.sourceforge.net/sourceforge/wicd/%{name}-%{version}.tar.gz
# Source0-md5:	dda372b0778de24552850d3d877d1b65
URL:		http://wicd.net/
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Wicd is an open source wired and wireless network manager for Linux
which aims to provide a simple interface to connect to networks with a
wide variety of settings.

%description -l pl.UTF-8
Wicd jest zarządcą sieci który stara się dostarczyć prosty
interfejs do podłączania do sieci z różnorakimi opcjami.

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


%clean
rm -rf $RPM_BUILD_ROOT

%pre
%postun

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/*.egg-info

%{_pixmapsdir}/%{module}
%{_mandir}
%{_datadir}/locale
%{_datadir}/%{module}
%{_iconsdir}/hicolor
/etc/dbus-1/system.d/wicd.conf
%{_sysconfdir}/wicd
%{_sysconfdir}/xdg/autostart/wicd-tray.desktop
%dir %{_libdir}/%{module}/
%attr(755,root,root) %{_libdir}/%{module}/*.py

%attr(755,root,root) %{_bindir}/wicd-client
%attr(755,root,root) %{_sbindir}/wicd
%{_desktopdir}/wicd.desktop
%{_datadir}/autostart/wicd-tray.desktop
/var/lib/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
