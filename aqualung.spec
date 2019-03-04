#https://github.com/jeremyevans/aqualung/commit/72c1ab19fc8cd3294d5d0a7fd676099cd26d72db
%global         commit0 72c1ab19fc8cd3294d5d0a7fd676099cd26d72db
%global         shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global         nonfree  0
%global         free     1

%if 0%{nonfree}
# "Monkey's Audio Source Code License Agreement" is nonfree license.
%global         with_mac  --with-mac
%endif

%if 0%{free}
# The following packages are free license (patent issue).
%global         with_mpeg --with-mpeg
%global         with_lavc --with-lavc
%global         with_lame --with-lame
%endif

Name:           aqualung
Version:        1.0
Release:        0.15.rc1git%{shortcommit0}%{?dist}
Summary:        Music Player for GNU/Linux
License:        GPLv2+
URL:            http://aqualung.jeremyevans.net/
Source0:        https://github.com/jeremyevans/aqualung/archive/%{commit0}/%{name}-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:        %{name}.desktop

# autogen.sh
BuildRequires:  autoconf automake pkgconfig gettext-devel
# GUI
BuildRequires:  glib2-devel gtk2-devel atk-devel cairo-devel pango-devel
BuildRequires:  pixman-devel libpng-devel zlib-devel
BuildRequires:  fontconfig-devel freetype-devel libxml2-devel
# Desktop
BuildRequires:  desktop-file-utils
# Output
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(samplerate)
# Encode/Decode
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  pkgconfig(oggz)
BuildRequires:  pkgconfig(speex)
%{?with_mpeg:BuildRequires:  pkgconfig(mad)}
BuildRequires:  pkgconfig(libmodplug)
BuildRequires:  libmpcdec-devel
%{?with_mac:BuildRequires:  pkgconfig(mac)}
%{?with_lavc:BuildRequires:  ffmpeg-devel}
%{?with_lame:BuildRequires:  lame-devel}
BuildRequires:  pkgconfig(wavpack)
BuildRequires:  pkgconfig(lrdf)
# CD
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  libcdio-paranoia-devel
BuildRequires:  pkgconfig(libcddb)
# Others
BuildRequires:  pkgconfig(libusb)
BuildRequires:  libifp-devel
BuildRequires:  pkgconfig(lua)

%description
Aqualung is an advanced music player originally targeted at the GNU/Linux
operating system. It plays audio CDs, internet radio streams and pod casts as
well as sound files in just about any audio format and has the feature of
inserting no gaps between adjacent tracks.

%prep
%setup -qn %{name}-%{commit0}

%build
./autogen.sh
%configure \
    --without-sndio \
    --with-oss \
    --with-alsa \
    --with-jack \
    --with-pulse \
    --with-src \
    --with-sndfile \
    --with-flac \
    --with-vorbisenc \
    --with-speex \
    %{!?with_mpeg: --without-mpeg} %{?with_mpeg} \
    --with-mod \
    --with-mpc \
    %{!?with_mac:  --without-mac} %{?with_mac} \
    %{!?with_lavc: --without-lavc} %{?with_lavc} \
    %{!?with_lame: --without-lame} %{?with_lame} \
    --with-wavpack \
    --with-ladspa \
    --with-cdda \
    --with-cddb \
    --with-ifp \
    --with-lua


# Fix lib64 path
sed -i 's@/usr/lib/@%{_libdir}/@g' src/plugin.c

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p -c"

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

install -d -m 755 %{buildroot}%{_datadir}/pixmaps
install -D -m 644 -p src/img/icon_48.png \
    %{buildroot}%{_datadir}/pixmaps/%{name}.png

%find_lang %{name}


%post
update-desktop-database &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :


%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*
%{_datadir}/man/man1/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_docdir}/%{name}

%changelog
* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0-0.15.rc1git72c1ab1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0-0.14.rc1git72c1ab1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.0-0.13.rc1git72c1ab1
- Rebuilt for new ffmpeg snapshot

* Wed Feb 28 2018 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0-0.12.rc1git72c1ab1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Sérgio Basto <sergio@serjux.com> - 1.0-0.11.rc1git72c1ab1
- Rebuild (libcdio)

* Wed Jan 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0-0.10.rc1git72c1ab1
- Rebuilt for ffmpeg-3.5 git

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0-0.9.rc1git72c1ab1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0-0.8.rc1git72c1ab1
- Rebuild for ffmpeg update

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0-0.7.rc1git72c1ab1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Martin Gansser <martinkg@fedoraproject.org> - 1.0-0.6.rc1git72c1ab1
- Update to 1.0-0.6.rc1git72c1ab1

* Thu Nov 17 2016 Adrian Reber <adrian@lisas.de> - 1.0-0.5.rc1git05dfcb7
- Rebuilt for libcdio-0.94

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-0.4.rc1git05dfcb7
- Rebuilt for ffmpeg-3.1.1

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-0.3.rc1git05dfcb7
- Rebuilt for ffmpeg-3.1.1

* Fri Jul 01 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.0-0.2.rc1git05dfcb7
- Switched from svn to git
- Update to 1.0-0.2.rc1git05dfcb7
- Added %%{_docdir}/%%{name}

* Fri Aug 28 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.0-0.1.svn1311
- Update to SVN r1311

* Mon Mar 02 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.9-0.8.svn1309
- dropped aqualung-fsf-fix.patch

* Sun Mar 01 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.9-0.7.svn1309
- added link to upstream patch %%{name}-fsf-fix.patch
- corrected lincese tag
- Mark license files as %%license where available
- dropped %%defattr does not need any longer
- dropped macro %%{buildroot}
- take ownership of unowned directory %%{_datadir}/%%{name}/
- added pkgconfig based BR

* Sun Mar 01 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.9-0.6.svn1309
- Update to SVN r1309.
- added BR libcdio-paranoia-devel
- dropped unrecognized %%configure options
- added %%{name}-fsf-fix.patch
- corrected license tag

* Tue Feb 2 2010 Akio Idehara <zbe64533 at gmail.com> 0.9-0.5.svn1115
- Disable mac support, this is mac's the license issue

* Mon Feb 1 2010 Akio Idehara <zbe64533 at gmail.com> 0.9-0.4.svn1115
- Add post/postun

* Mon Feb 1 2010 Akio Idehara <zbe64533 at gmail.com> 0.9-0.3.svn1115
- Update to SVN r1115

* Sun Jan 31 2010 Akio Idehara <zbe64533 at gmail.com> 0.9-0.2.svn1109
- Change Socket test routine

* Sat Jan 23 2010 Akio Idehara <zbe64533 at gmail.com> 0.9-0.1.svn1109
- Initial RPM release
