# TODO
# - fix pm-utils to store addons in non-arch dependant path so we could make this pkg noarch
# - package (acpid-XXX):
#   /etc/acpi/resume.d/80-wicd-connect.sh
#   /etc/acpi/suspend.d/50-wicd-suspend.sh
# - now python libraries installs into /usr/share/wicd by default, so I commented libexecdir redefinition. but its now easy to revert and change install behaviour simply uncomenting it
# - translations installing is broken. fr and FR both exists, hack with renaming doesnt work for hr_HR and ar_PS isnt in glibc yet. something is really fucked up, because I cannot find fr_FR nowhere in source dir (find + grep), but instalation creates empty dirs that break installation later :/

Summary:	wired and wireless network manager
Summary(pl.UTF-8):	Zarządca sieci przewodowych i bezprzewodowych
Name:		wicd
Version:	1.7.0
Release:	0.1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/wicd/%{name}-%{version}.tar.gz
# Source0-md5:	003d2e67240989db55934553437ba32a
Source1:	%{name}.init
Patch0:		%{name}-init_status.patch
Patch1:		bashism.patch
URL:		http://www.wicd.net/
# /etc/pld-release used to detect platform
BuildRequires:	issue
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	dbus(org.freedesktop.Notifications)
Requires:	python-dbus
Requires:	python-iwscan
Requires:	python-pygobject
Requires:	python-pygtk-glade >= 2:2.0
Requires:	python-pygtk-gtk >= 2:2.0
Requires:	python-wpactrl
# not noarch due pm-utils packaging stupidity
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#%define		_libexecdir	%{_prefix}/lib/%{name}

%description
Wicd is an open source wired and wireless network manager for Linux
which aims to provide a simple interface to connect to networks with a
wide variety of settings.

%description -l pl.UTF-8
Wicd jest zarządcą sieci przewodowych i bezprzewodowych dla Linuksa,
mającym zapewnić prosty interfejs do podłączania do sieci z
różnorakimi opcjami.

%package client-cli
Summary:	wicd CLI client
Summary(pl.UTF-8):	klient wicd CLI
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	python-urwid

%description client-cli
Wicd command line interface (ncurses) client.

%description client-cli -l pl.UTF-8
Klient wicd z międzymordziem wiersza poleceń (ncurses).

%package client-curses
Summary:	wicd TUI client
Summary(pl.UTF-8):	klient wicd z TUI
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description client-curses
Wicd text user interface (ncurses) client.

%description client-curses -l pl.UTF-8
Klient Wicd z tesktowym międzymordziem uzytkownika (ncurses).

%package client-gtk
Summary:	wicd GUI client
Summary(pl.UTF-8):	klient wicd z GUI
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description client-gtk
Wicd graphical user interface (GTK+2) client.

%description client-gtk -l pl.UTF-8
Klient Wicd z graficznym międzymordziem użytkownika (GTK+2).

%package -n pm-utils-wicd
Summary:	wicd script for pm-utils
Summary(pl.UTF-8):	Skrypt wicd dla pm-utils
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	pm-utils

%description -n pm-utils-wicd
Wicd script for pm-utils.

%description -n pm-utils-wicd -l pl.UTF-8
Skrypt wicd dla pm-utils.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

mv translations/{ar_EG,ar} # WTF? Then what do with ar_PS?
rm -rf translations/ar_PS # so removing it temporary until somebody put those dirs into glibc
mv translations/{de_DE,de}
mv translations/{es_ES,es}
rm -rf translations/fr
mv translations/{fr_FR,fr} # We got serious problem there, because both fr and fr_FR exsists and differs
#mv translations/{hr_HR,hr} # Doesnt work for me
mv translations/{it_IT,it}
mv translations/{nl_NL,nl}
mv translations/{no,nb}
mv translations/{ru_RU,ru}

grep -r bin/env.*python -l . | xargs sed -i -e '1s,^#!.*env python,#!%{__python},'

%build
%{__python} setup.py configure \
	--backends %{_libexecdir}/backends \
	--cli %{_libexecdir}/cli \
	--curses %{_libexecdir}/curses \
	--daemon %{_libexecdir}/daemon \
	--gtk %{_libexecdir}/gtk \
	--pidfile /var/run/wicd.pid \
	--pmutils %{_libdir}/pm-utils/sleep.d

%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/wicd

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
%{_mandir}/man5/wicd-manager-settings.conf.5*
%lang(nl) %{_mandir}/nl/man5/wicd-manager-settings.conf.5*
%{_mandir}/man5/wicd-wired-settings.conf.5*
%lang(nl) %{_mandir}/nl/man5/wicd-wired-settings.conf.5*
%{_mandir}/man5/wicd-wireless-settings.conf.5*
%lang(nl) %{_mandir}/nl/man5/wicd-wireless-settings.conf.5*
%{_mandir}/man8/wicd.8*
%lang(nl) %{_mandir}/nl/man8/wicd.8*
/etc/dbus-1/system.d/wicd.conf
%{_sysconfdir}/wicd
%{_sysconfdir}/xdg/autostart/wicd-tray.desktop
%dir %{_libexecdir}
%dir %{_libexecdir}/backends
%attr(755,root,root) %{_libexecdir}/backends/*.py
%dir %{_libexecdir}/daemon
%attr(755,root,root) %{_libexecdir}/daemon/*.py
%dir %{py_sitescriptdir}/wicd
%{py_sitescriptdir}/wicd/*.py[co]
%{py_sitescriptdir}/Wicd-*.egg-info
%dir /var/lib/%{name}
/var/lib/%{name}/WHEREAREMYFILES
%dir /var/log/%{name}

%files client-cli
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wicd-cli
%dir %{_libexecdir}/cli
%attr(755,root,root) %{_libexecdir}/cli/*.py
%{_mandir}/man8/wicd-cli.8*

%files client-curses
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wicd-curses
%dir %{_libexecdir}/curses
%attr(755,root,root) %{_libexecdir}/curses/*.py
%{_mandir}/man8/wicd-curses.8*
%lang(nl) %{_mandir}/nl/man8/wicd-curses.8*

%files client-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wicd-gtk
%dir %{_libexecdir}/gtk
%{_libexecdir}/gtk/%{name}.glade
%attr(755,root,root) %{_libexecdir}/gtk/*.py
%{_datadir}/autostart/wicd-tray.desktop
%{_desktopdir}/wicd.desktop
%{_iconsdir}/hicolor/*/apps/wicd-gtk.*
%{_pixmapsdir}/%{name}
%{_pixmapsdir}/wicd-gtk.xpm
%{_mandir}/man1/wicd-client.1*
%lang(nl) %{_mandir}/nl/man1/wicd-client.1*

%files -n pm-utils-wicd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pm-utils/sleep.d/*wicd
