#
###############################################################################

INSTALL=$(shell cd .. ; /bin/pwd)
SHARE=$(INSTALL)/share
PACKAGE := $(shell cd .. ; basename `/bin/pwd`)

export MYOS	:= $(shell uname -s)
export ARCH	:= $(shell uname -m)

ifeq "$(MYOS)" "Linux"
  export AR   = /usr/bin/ar
  export INST = /usr/bin/install
else
  export AR   = /usr/ccs/bin/ar
  export INST = /usr/local/bin/install
endif

RM      = /bin/rm -f

# Target macros (what we are to build/install)
CONFS	=
IDLFILES=
LIBEXECS=
LIBRARIES=
MAN1	= 
MAN3	=
MAN5	=
OBJS	= 
PROGS	= primes
SCRIPTS	= 

# C Compilation macros
CC	= cc
# JSW: Optimized program runs a tad faster.
CFLAGS	= -O -g -lm
DEFINES =
INCLUDES=
LDFLAGS	=
LIBS	=

COMPILE	= $(CC) $(CFLAGS) $(DEFINES) $(INCLUDES)

# Install directories
BINDIR	= $(INSTALL)/$(ARCH)/bin
IDLDIR  = $(SHARE)/idl/$(PACKAGE)
CONFDIR = $(SHARE)/config
LIBEXECDIR = $(INSTALL)/$(ARCH)/libexec/$(PACKAGE)
LIBDIR	= $(INSTALL)/$(ARCH)/lib
MAN1DIR = $(SHARE)/man/man1
MAN3DIR = $(SHARE)/man/man3
MAN5DIR = $(SHARE)/man/man5

# Targets
all: $(CONFS) $(LIBEXECS) $(MAN1) $(MAN3) $(MAN5) $(OBJS) $(PROGS) $(SCRIPTS)

clean:
	$(RM) $(CONFS) $(LIBEXECS) $(LIBRARIES) $(OBJS) $(PROGS) \
	$(IDLFILES) $(SCRIPTS)

install: all installdirs \
	$(CONFS:%=$(CONFDIR)/%) \
	$(IDLFILES:%=$(IDLDIR)/%) \
	$(LIBEXECS:%=$(LIBEXECDIR)/%) \
	$(LIBRARIES:%=$(LIBDIR)/%) \
	$(MAN1:%=$(MAN1DIR)/%) \
	$(MAN3:%=$(MAN3DIR)/%) \
	$(MAN5:%=$(MAN5DIR)/%) \
	$(PROGS:%=$(BINDIR)/%) \
	$(SCRIPTS:%=$(BINDIR)/%) 

installdirs:
	mkappdirs -a $(ARCH) ..

# Build Rules


# general rule for C code
% : %.c
	$(CC) $(CFLAGS) $(DEFINES) $(INCLUDES) $(LIBS) -o $@ $<

# Config files
%.conf : %.conf.in
	cat $< > $@

# Install rules

# create target dir if it doesn't exist
checkdir = if [ ! -d $(1) ]; then mkdir -p $(1); chmod 755 $(1) ; fi

$(BINDIR)/%: %
	$(call checkdir,$(BINDIR))
	$(INST) -m 755 $< $(BINDIR)

$(CONFDIR)/%: %
	$(call checkdir,$(CONFDIR))
	$(INST) -m 644 $< $(CONFDIR)

$(IDLDIR)/%: %
	$(call checkdir,$(IDLDIR))
	$(INST) -m 644 $< $(IDLDIR)

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

