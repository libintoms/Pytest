from OpenSSL import SSL
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna
from socket import socket
from collections import namedtuple

class SSLCheck :

    def __init__(self,hostname, port) -> None:
        
        self.hostname = hostname
        self.port = port
        self.certificate = ''
        self.peername = ''

    def get_certificate(self):

        hostname_idna = idna.encode(self.hostname)
        sock = socket()

        sock.connect((self.hostname, self.port))
        self.peername = sock.getpeername()
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.set_verify(SSL.VERIFY_NONE)
        ctx.check_hostname = False

        sock_ssl = SSL.Connection(ctx, sock)
        sock_ssl.set_connect_state()
        sock_ssl.set_tlsext_host_name(hostname_idna)
        sock_ssl.do_handshake()
        self.cert = sock_ssl.get_peer_certificate()
        self.certificate = self.cert.to_cryptography()
        sock_ssl.close()
        sock.close()    

    def get_alt_names(self):
        try:
            ext = self.certificate.extensions.get_extension_for_class(x509.SubjectAlternativeName)
            return ext.value.get_values_for_type(x509.DNSName)
        except x509.ExtensionNotFound:
            return None

    def get_common_name(self):
        try:
            names = self.certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
            return names[0].value
        except x509.ExtensionNotFound:
            return None

    def get_issuer(self):
        try:
            names = self.certificate.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
            return names[0].value
        except x509.ExtensionNotFound:
            return None

    def print_host_info(self):
        self.get_certificate()

        output = '''
        Hostname: {hostname} \n 
        Port: {port}\n
        Peername: {peername}\n
        Common Name: {common_name}\n
        SAN: {san}\n
        Issuer: {issuer}\n
        Not Before: {not_before}\n
        Not After: {not_after}
        '''.format(hostname=self.hostname, 
            port=self.port, 
            peername=self.peername,
            common_name=self.get_common_name(),
            san=self.get_alt_names(),
            issuer=self.get_issuer(),
            not_before=self.certificate.not_valid_before,
            not_after=self.certificate.not_valid_after)

        # print(self.hostname, self.port, self.peername, self.get_common_name(), self.get_alt_names(), self.get_issuer())
        print(output)


