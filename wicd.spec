# TODO: Fix files list
Summary:	wired and wireless network manager
Summary(pl.UTF-8):	Zarządca sieci przewodowych i bezprzewodowych
Name:		wicd
Version:	1.5.9
Release:	2
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/wicd/%{name}-%{version}.tar.gz
# Source0-md5:	4743a30eb8e3898b8b1a319b0c373ce5
Patch0:		%{name}-init_status.patch
URL:		http://wicd.net/
# /etc/pld-release used to detect platform
BuildRequires:	issue
BuildRequires:	python-devel
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
%patch0 -p1

%{__python} setup.py configure \
	--pidfile /var/run/wicd.pid

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

# no other ar exists here
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{ar_EG,ar}
# bg_BG is empty, it will not be packaged
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{bg,bg_bogus}
# bogus? but see above
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{bg_PHO,bg}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{ca_ES,ca}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{cs_CZ,cs}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{da_DK,da}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{el_GR,el}
# duplicate of gl_ES
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/es_GL
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{et_EE,et}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{eu_ES,eu}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{gl_ES,gl}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{ko_KR,ko}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{ml_IN,ml}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{no,nb}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{sl_SI,sl}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{sp_MX,es_MX}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{sv_SE,sv}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{te_IN,te}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{ua,uk}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{vi_VN,vi}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{fa_IR,fa}


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
/var/log/%{name}
%{_mandir}/man1/wicd-client.1*
%{_mandir}/man5/wicd-manager-settings.conf.5*
%{_mandir}/man5/wicd-wired-settings.conf.5*
%{_mandir}/man5/wicd-wireless-settings.conf.5*
%{_mandir}/man8/wicd.8*
