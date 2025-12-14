from django.db import models
from django.db.models.functions import Cast
from django.db.models import TextField

class Lease4(models.Model):
    address = models.BigIntegerField(primary_key=True) # bigint NOT NULL, PRIMARY KEY
    hwaddr = models.BinaryField(blank=True, null=True) # bytea
    client_id = models.BinaryField(blank=True, null=True) # bytea
    valid_lifetime = models.BigIntegerField(blank=True, null=True) # bigint
    expire = models.DateTimeField(blank=True, null=True) # timestamp with time zone
    subnet_id = models.BigIntegerField(blank=True, null=True) # bigint
    fqdn_fwd = models.BooleanField(blank=True, null=True) # boolean
    fqdn_rev = models.BooleanField(blank=True, null=True) # boolean
    hostname = models.CharField(max_length=255, blank=True, null=True) # character varying(255)
    state = models.BigIntegerField(default=0) # bigint DEFAULT 0
    user_context = models.TextField(blank=True, null=True) # text
    relay_id = models.BinaryField(blank=True, null=True) # bytea
    remote_id = models.BinaryField(blank=True, null=True) # bytea
    pool_id = models.BigIntegerField(default=0) # bigint NOT NULL DEFAULT 0

    class Meta:
        db_table = 'lease4'  # Actual table name in PostgreSQL
        managed = False

    def __str__(self):
        return self.ipv4addr  # Will use ipv4addr property

    @property
    def ipv4addr(self):
        # SQL: '0.0.0.0'::inet + address
        return str(models.F("address") + 0) # Django ORM way to do integer addition in query, then cast to string for display

    @property
    def hwaddr_formatted(self):
        if self.hwaddr:
            # SQL: colonseparatedhex(encode(hwaddr, 'hex'::text))
            import binascii
            hex_encoded = binascii.hexlify(self.hwaddr).decode('utf-8')
            return ":".join(hex_encoded[i:i+2] for i in range(0, len(hex_encoded), 2))
        return ""

    @property
    def clientid_formatted(self):
        if self.client_id:
            # SQL: colonseparatedhex(encode(client_id, 'hex'::text))
            import binascii
            hex_encoded = binascii.hexlify(self.client_id).decode('utf-8')
            return ":".join(hex_encoded[i:i+2] for i in range(0, len(hex_encoded), 2))
        return ""

