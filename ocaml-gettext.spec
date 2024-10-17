%define name    ocaml-gettext
%define version 0.3.3
%define release %mkrel 2

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        OCaml library for i18n
Group:          Development/Other
License:        LGPLv2+ with exceptions
URL:            https://sylvain.le-gall.net/ocaml-gettext.html
Source0:        http://sylvain.le-gall.net/download/%{name}-%{version}.tar.gz
Requires:       ocaml-camomile-data
BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib
BuildRequires:  camlp4
BuildRequires:  ocaml-fileutils-devel
BuildRequires:  ocaml-camlidl-devel
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-camomile-devel
BuildRequires:  ocaml-camomile-data
BuildRequires:  docbook-dtd43-xml
BuildRequires:  docbook-style-xsl
BuildRequires:  libxslt-proc
BuildRequires:  chrpath
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
Ocaml-gettext provides support for internationalization of Ocaml
programs.

Constraints :

* provides a pure Ocaml implementation,
* the API should be as close as possible to GNU gettext,
* provides a way to automatically extract translatable
  strings from Ocaml source code.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}
Requires:       ocaml-fileutils-devel


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        camomile
Summary:        Parts of %{name} which depend on Camomile
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description    camomile
The %{name}-camomile package contains the parts of %{name} which
depend on Camomile.

%package        camomile-devel
Summary:        Development files for %{name}-camomile
Group:          Development/Other
Requires:       %{name}-devel = %{version}-%{release}


%description    camomile-devel
The %{name}-camomile-devel package contains libraries and
signature files for developing applications that use
%{name}-camomile.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
  --libdir=%{_libdir} \
  --with-docbook-stylesheet=/usr/share/sgml/docbook/xsl-stylesheets \
  --enable-test
make

%check
pushd test
../_build/bin/test
popd

%install
rm -rf %{buildroot}

# make install in the package is screwed up completely.  Install
# by hand instead.
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
mkdir -p %{buildroot}%{_bindir}

# Remove *.o files - these shouldn't be distributed.
find _build -name '*.o' -exec rm {} \;

ocamlfind install gettext _build/lib/gettext/*
ocamlfind install gettext-stub _build/lib/gettext-stub/*
ocamlfind install gettext-camomile _build/lib/gettext-camomile/*
install -m 0755 _build/bin/ocaml-gettext %{buildroot}%{_bindir}
install -m 0755 _build/bin/ocaml-xgettext %{buildroot}%{_bindir}

strip $OCAMLFIND_DESTDIR/stublibs/dll*.so
chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so
strip %{buildroot}%{_bindir}/ocaml-gettext


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc COPYING
%{_libdir}/ocaml/gettext
%{_libdir}/ocaml/gettext-stub
%exclude %{_libdir}/ocaml/gettext/*.a
%exclude %{_libdir}/ocaml/gettext/*.cmxa
%exclude %{_libdir}/ocaml/gettext/*.cmx
%exclude %{_libdir}/ocaml/gettext-stub/*.a
%exclude %{_libdir}/ocaml/gettext-stub/*.cmxa
%exclude %{_libdir}/ocaml/gettext-stub/*.cmx
%exclude %{_libdir}/ocaml/gettext/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%defattr(-,root,root)
%doc README CHANGELOG TODO
# %doc build/share/doc/html/*
%{_libdir}/ocaml/gettext/*.a
%{_libdir}/ocaml/gettext/*.cmxa
%{_libdir}/ocaml/gettext/*.cmx
%{_libdir}/ocaml/gettext-stub/*.a
%{_libdir}/ocaml/gettext-stub/*.cmxa
%{_libdir}/ocaml/gettext-stub/*.cmx
%{_libdir}/ocaml/gettext/*.mli
%{_bindir}/ocaml-gettext
%{_bindir}/ocaml-xgettext

%files camomile
%defattr(-,root,root)
%doc COPYING
%{_libdir}/ocaml/gettext-camomile
%exclude %{_libdir}/ocaml/gettext-camomile/*.a
%exclude %{_libdir}/ocaml/gettext-camomile/*.cmxa
%exclude %{_libdir}/ocaml/gettext-camomile/*.cmx
%exclude %{_libdir}/ocaml/gettext-camomile/*.mli

%files camomile-devel
%defattr(-,root,root)
%doc README
%{_libdir}/ocaml/gettext-camomile/*.a
%{_libdir}/ocaml/gettext-camomile/*.cmxa
%{_libdir}/ocaml/gettext-camomile/*.cmx
%{_libdir}/ocaml/gettext-camomile/*.mli

