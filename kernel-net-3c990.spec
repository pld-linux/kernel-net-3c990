
# conditional build
# _without_dist_kernel          without distribution kernel

%define		_orig_name	3c990
%define		_rel 6

Summary:	Linux driver for the 3Com 3C990 Network Interface Cards
Summary(pl):	Sterownik dla Linuksa do kart sieciowych 3Com 3C990
Name:		kernel-net-%{_orig_name}
Version:	1.0.0a
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://support.3com.com/infodeli/tools/nic/linux/%{_orig_name}-%{version}.tar.gz
Patch0:		%{_orig_name}-redefine.patch
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
BuildRequires:	%{kgcc_package}
PreReq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This driver (3c990.c) has been written to work with the 3c990 product
line of network cards, manufactured by 3Com Corp.

This driver is not intended for any other product line, including the
3c59x or 3c90x product lines (although drivers with both of these
names, and for both of these product lines, are available). 

%description -l pl
Sterownik dla Linuksa do kart sieciowych 3Com 3c990.

Nie obs³uguje kart serii 3c59x i 3c90x, istniej± inne sterowniki do
tych linii produktów.

%package -n kernel-smp-net-%{_orig_name}
Summary:        Linux SMP driver for the 3Com 3C990 Network Interface Cards
Summary(pl):    Sterownik dla Linuxa SMP dla kart sieciowych 3Com 3C990
Release:        %{_rel}@%{_kernel_ver_str}
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Group:		Base/Kernel

%description -n kernel-smp-net-%{_orig_name}
This driver (3c990.c) has been written to work with the 3c990 product
line of network cards, manufactured by 3Com Corp on SMP systems.

This driver is not intended for any other product line, including the
3c59x or 3c90x product lines (although drivers with both of these
names, and for both of these product lines, are available).

%description -n kernel-smp-net-%{_orig_name} -l pl
Sterownik dla Linuksa SMP do kart sieciowych 3Com 3c990.

Nie obs³uguje kart serii 3c59x i 3c90x, istniej± inne sterowniki do
tych linii produktów.

%prep
%setup -q -n %{_orig_name}-%{version} -c
%patch0 -p0

%build
rm -f %{_orig_name}.o
%{kgcc} -o %{_orig_name}.o -c %{rpmcflags}  -c -DMODULE -D__KERNEL__ -O2 -DSMP=1 -D__SMP__ -DCONFIG_X86_LOCAL_APIC -Wall -Wstrict-prototypes -I%{_kernelsrcdir}/include %{_orig_name}.c
mv -f %{_orig_name}.o %{_orig_name}-smp.o
%{kgcc} -o %{_orig_name}.o -c %{rpmcflags}  -c -DMODULE -D__KERNEL__ -O2 -Wall -Wstrict-prototypes -I%{_kernelsrcdir}/include %{_orig_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

install %{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o
install %{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o

gzip -9nf README

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a

%postun -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.gz
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
%doc *.gz 
/lib/modules/%{_kernel_ver}smp/misc/*
