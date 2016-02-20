# H+
#       Title   : Makefile
#       Author  : Steve Carson (from code by Jerel Moffatt)
#       Date    : 2015-08-20
#       Synopsis: Makefile for "primes"
#       $Date: 2015/08/25 19:25:37 $
#       $Revision: 1.2 $
#	$Source: /lasp/software/src/gold/cmd_tools/src/Makefile,v $
#	$Locker:  $
#
#       Revisions:
#       YYYY-MM-DD  WHO DESCRIPTION
#       2015-08-20  sgc Initial version cloned from PODA
# H-
# E+ 
#   % make all	
#	builds the whole hierarchy using default rules (normally "all") in
#	directories defined by SUBDIRS
#   % make clean
#	cleans out all generated/compiled files from the whole hierarchy
#   % make clean-directory
#	cleans out all generated/compiled files from the specified subdirectory
#	hierarchy
#   % make directory
#	builds a single directory hierarchy using default rules in the
#	subdirectories
#   % make install
#	builds and installs the whole hierarchy by triggering the default
#	rules in any subdirectory (due to dependency of "all" in top level
#	makefile which includes the dependency SUBDIRS), then calls
#	the install rule in the subdirectories, each of which normally has the 
#	dependency of "all" as well, causing "all" to be built if not
#	previously done, then finally installs all of the files.
#   % make install-directory
#	builds and installs a single subdirectory hierarchy using the "install"
#	target in the subdirectory (which normally should have the dependency
#	"all")
# E-
#
###############################################################################

# define parameters required by sub-makes
export TOP      := $(shell /bin/pwd)
export INSTALL	:= $(shell cd .. ; /bin/pwd)
export SHARE	:= $(INSTALL)/share

### Uncomment one of the following if desired (see Install Directories below)
# Versionless PACKAGE definition
export PACKAGE	:= primes

# version for the directory contained in the distribution file for the
# web Managed via external file which should be updated whenever you
# update the code base.
export VERSION = $(shell cat ../version.txt)

export ARCH	:= $(shell uname -m)
export INST	= install

# forcibly unset LD_LIBRARY_PATH so it doesn't interfere with compilation
export LD_LIBRARY_PATH=

RM = rm -f

# list of general files created with pattern substitution via sed
INPUT_FILES=$(shell /bin/ls *.in 2>/dev/null)
GENERATED=$(INPUT_FILES:%.in=%)

# Target macros (what we are to build/install) 
##############################################
HEADERS =
IDLFILES=
PYTHONFILES = \
	primeslib.py \
	errmsgs.py \
	../version.txt
PYTHONCONFS = \
	primes.conf
JARS        =
JSRCS       =
JCLASSES    =
LIBEXECS    =
LIBRARIES   =
MAN1        = 
MAN3        =
MAN5        =
OBJS        = 
PROGS       =
SCRIPTS     = \
	primes

# Compilation macros
####################
CC          =
CFLAGS      =
CLASSPATH   = -classpath .
DEFINES     =
INCLUDES    =
JAVAC       = javac $(CLASSPATH)
LDFLAGS     =
LIBS        =

COMPILE	= $(CC) $(CFLAGS) $(DEFINES) $(INCLUDES)


# Install directories
#####################
export BINDIR	  := $(INSTALL)/$(ARCH)/bin
export CONFDIR	  := $(SHARE)/config
export DATADIR	  := $(SHARE)/data/$(PACKAGE)
export DOCDIR	  := $(SHARE)/doc/$(PACKAGE)
export IDLDIR	  := $(SHARE)/idl/
export PYTHONDIR  := $(SHARE)/python/$(PACKAGE)
export INCLUDEDIR := $(INSTALL)/include
export JAVADIR	  := $(SHARE)/java/$(PACKAGE)
export LIBEXECDIR := $(INSTALL)/$(ARCH)/libexec/$(PACKAGE)
export LIBDIR	  := $(INSTALL)/$(ARCH)/lib
export MAN1DIR	  := $(SHARE)/man/man1
export MAN3DIR	  := $(SHARE)/man/man3
export MAN5DIR	  := $(SHARE)/man/man5
export WEBDIR	  = $(PACKAGE)_$(VERSION)


# Targets
#########
# allow subdirs to be built individually for testing (ie. cd dir ; make all)
.PHONY  : $(SUBDIRS)

# SUBDIRS dependency will build default target in those directories
all: $(CONFS) $(IDLFILES) $(OBJS) $(LIBRARIES) $(LIBEXECS) $(MAN1) $(MAN3) \
	$(MAN5) $(PROGS) $(SCRIPTS) ${PYTHONFILES}

# Clean up subdirectories first, then specified files
clean: 
	$(RM) $(JARS) $(LIBEXECS) $(LIBRARIES) $(OBJS) $(PROGS) \
	$(SCRIPTS) $(GENERATED) $(WEB_TAR)
	/bin/rm -rf $(WEBDIR)

# Clean up subdirectories first, then specified files
clean_install:
	$(RM) $(JARS) $(LIBEXECS) $(LIBRARIES) $(OBJS) $(PROGS) \
	$(SCRIPTS) $(GENERATED); \
	rm -rf __pycache__ $(SHARE) $(INSTALL)/$(ARCH) $(INSTALL)/include

# Install the files (subdirs will be installed last so targets there can have
# dependencies on files higher up in the hierarchy)
install: all installdirs \
	$(CONFS:%=$(CONFDIR)/%) \
	$(JARS:%=$(JAVADIR)/%) \
	$(IDLFILES:%=$(IDLDIR)/%) \
	$(PYTHONFILES:%=$(BINDIR)/%)\
	$(PYTHONCONFS:%=$(BINDIR)/%)\
	$(HEADERS:%=$(INCLUDEDIR)/%) \
	$(LIBEXECS:%=$(LIBEXECDIR)/%) \
	$(LIBRARIES:%=$(LIBDIR)/%) \
	$(MAN1:%=$(MAN1DIR)/%)	\
	$(MAN3:%=$(MAN3DIR)/%)	\
	$(MAN5:%=$(MAN5DIR)/%) \
	$(PROGS:%=$(BINDIR)/%) \
	$(SCRIPTS:%=$(BINDIR)/%)

# create a standard hierarchy of install directories
installdirs:
	mkappdirs -a $(ARCH) ..

# Build Rules 
########################

# local setup file for testing
local_setup.csh:
	mklocalsetup > $@

local_setup.bourne:
	mklocalsetup sh > $@


# build executable scrips from *.sh files using pattern substitution
% : %.sh
	sed \
		-e 's#xxIDLPATHxx#$(IDLPATH)#g' \
		-e 's#xxJAVADIRxx#$(JAVADIR)#g' \
		-e 's#xxLIBEXECDIRxx#$(LIBEXECDIR)#g' \
		$< > $@
	chmod +x $@


# build executable scrips from *.py files using pattern substitution
% : %.py
	sed \
		-e 's#xxVERSIONxx#$(VERSION)#g' \
		-e 's#xxPYTHONDIRxx#$(PYTHONDIR)#g' \
		$< > $@
	chmod +x $@


# general rule for C code
% : %.c
	$(CC) $(CFLAGS) $(DEFINES) $(INCLUDES) $(LIBS) -o $@ $<

# Java code
%.class : %.java
	$(JAVAC) $<

# Java archive: change "foo" to whatever your jar file name is (see JARS)
foo.jar : $(CLASSES)
	$(JAVAC) $<

# Non executable files which require pattern substitution
% : %.in
	sed -e 's#xxIDLDIRxx#$(IDLDIR)#g' \
		-e 's#xxBINDIRxx#$(BINDIR)#g' \
		-e 's#xxLIBDIRxx#$(LIBDIR)#g' \
		$< > $@

# Install rules
###############

# create target dir if it doesn't exist
checkdir = @if [ ! -d $(1) ]; then mkdir -p -m 755 $(1) ; fi

$(BINDIR)/%: %
	$(call checkdir,$(BINDIR))
	$(INST) -m 755 $< $(BINDIR)

$(CONFDIR)/%: %
	$(call checkdir,$(CONFDIR))
	$(INST) -m 644 $< $(CONFDIR)

$(IDLDIR)/%: %
	$(call checkdir,$(IDLDIR))
	$(INST) -m 644 $< $(IDLDIR)

$(INCLUDEDIR)/%: %
	$(call checkdir,$(INCLUDEDIR))
	$(INST) -m 644 $< $(INCLUDEDIR)

$(JAVADIR)/%: %
	$(call checkdir,$(JAVADIR))
	$(INST) -m 644 $< $(JAVADIR)

$(PYTHONDIR)/%: %
	$(call checkdir,$(PYTHONDIR))
	$(INST) -m 644 $< $(PYTHONDIR)

$(LIBDIR)/%: %
	$(INST) -m 644 $< $(LIBDIR)

$(LIBEXECDIR)/%: %
	$(INST) -m 755 $< $(LIBEXECDIR)

$(MAN1DIR)/% : %
	sed -e 's#xxREVDATExx#'`gawk '/Date:/ { printf("%s",$$3) }' $< `'#' \
	< $< > $@ 
	chmod 644 $@

$(MAN3DIR)/% : %
	sed -e 's#xxREVDATExx#'`gawk '/Date:/ { printf("%s",$$3) }' $< `'#' \
	< $< > $@ 
	chmod 644 $@

$(MAN5DIR)/% : %
	sed -e 's#xxREVDATExx#'`gawk '/Date:/ { printf("%s",$$3) }' $< `'#' \
	< $< > $@ 
	chmod 644 $@
