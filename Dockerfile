FROM andrius/asterisk

COPY sip.conf /etc/asterisk/sip.conf
COPY extensions.conf /etc/asterisk/extensions.conf
