# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0029_auto_20150119_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='location',
            field=models.CharField(default=None, max_length=20, null=True, blank=True, choices=[(b'', b''), (b'BauerWarehouse', b'Bauer Warehouse'), (b'Surplussed', b'Surplussed'), (b'Other', b'Other'), (b'DC1704', b'DC-1704'), (b'DC1708', b'DC-1708'), (b'DC1709', b'DC-1709'), (b'DWE1535', b'DWE-1535'), (b'DWE3508', b'DWE-3508'), (b'DWE3509', b'DWE-3509'), (b'E21304', b'E2-1304'), (b'E32102A', b'E3-2102A'), (b'E32103', b'E3-2103'), (b'E32103A', b'E3-2103A'), (b'E32103B', b'E3-2103B'), (b'E32103C', b'E3-2103C'), (b'E32103D', b'E3-2103D'), (b'E32103G', b'E3-2103G'), (b'E32103H', b'E3-2103H'), (b'E32103M', b'E3-2103M'), (b'E32103N', b'E3-2103N'), (b'E32105', b'E3-2105'), (b'E32105A', b'E3-2105A'), (b'E32105B', b'E3-2105B'), (b'E32105F', b'E3-2105F'), (b'E32106', b'E3-2106'), (b'E32106B', b'E3-2106B'), (b'E32106C', b'E3-2106C'), (b'E32106D', b'E3-2106D'), (b'E32107', b'E3-2107'), (b'E32108', b'E3-2108'), (b'E32108B', b'E3-2108B'), (b'E32108C', b'E3-2108C'), (b'E32108D', b'E3-2108D'), (b'E32108E', b'E3-2108E'), (b'E32108F', b'E3-2108F'), (b'E32108G', b'E3-2108G'), (b'E32108K', b'E3-2108K'), (b'E32110', b'E3-2110'), (b'E32110A', b'E3-2110A'), (b'E32110B', b'E3-2110B'), (b'E32110C', b'E3-2110C'), (b'E32111', b'E3-2111'), (b'E32111B', b'E3-2111B'), (b'E32111C', b'E3-2111C'), (b'E32116', b'E3-2116'), (b'E32116A', b'E3-2116A'), (b'E32117', b'E3-2117'), (b'E32117A', b'E3-2117A'), (b'E32117B', b'E3-2117B'), (b'E32118', b'E3-2118'), (b'E32118A', b'E3-2118A'), (b'E32118B', b'E3-2118B'), (b'E32118C', b'E3-2118C'), (b'E32118D', b'E3-2118D'), (b'E32118E', b'E3-2118E'), (b'E32118F', b'E3-2118F'), (b'E32118G', b'E3-2118G'), (b'E32118H', b'E3-2118H'), (b'E32118J', b'E3-2118J'), (b'E32118K', b'E3-2118K'), (b'E32118W', b'E3-2118W'), (b'E32119', b'E3-2119'), (b'E32119A', b'E3-2119A'), (b'E32119B', b'E3-2119B'), (b'E32119C', b'E3-2119C'), (b'E32120', b'E3-2120'), (b'E32121N', b'E3-2121N'), (b'E32133', b'E3-2133'), (b'E32133B', b'E3-2133B'), (b'E32133C', b'E3-2133C'), (b'E32133D', b'E3-2133D'), (b'E32134', b'E3-2134'), (b'E32135C', b'E3-2135C'), (b'E32136', b'E3-2136'), (b'E32136F', b'E3-2136F'), (b'E32137', b'E3-2137'), (b'E32144', b'E3-2144'), (b'E32150', b'E3-2150'), (b'E32165A', b'E3-2165A'), (b'E32168', b'E3-2168'), (b'E32169', b'E3-2169'), (b'E32171', b'E3-2171'), (b'E32172', b'E3-2172'), (b'E33155', b'E3-3155'), (b'E33164', b'E3-3164'), (b'E33175', b'E3-3175'), (b'E33178', b'E3-3178'), (b'E33178A', b'E3-3178A'), (b'E33180', b'E3-3180'), (b'E34101', b'E3-4101'), (b'E34112', b'E3-4112'), (b'E53008', b'E5-3008'), (b'E53014', b'E5-3014'), (b'E53044', b'E5-3044'), (b'E53049', b'E5-3049'), (b'FRF102', b'FRF-102'), (b'FRF107', b'FRF-107'), (b'FRF109', b'FRF-109'), (b'FRF110', b'FRF-110'), (b'FRF111', b'FRF-111'), (b'FRF111A', b'FRF-111A'), (b'FRF111B', b'FRF-111B'), (b'FRF111C', b'FRF-111C'), (b'ERC2001', b'ERC-2001'), (b'ERC2006', b'ERC-2006'), (b'ERC2009', b'ERC-2009'), (b'ERC2011', b'ERC-2011'), (b'ERC2033', b'ERC-2033'), (b'ERC3003', b'ERC-3003'), (b'ERC3009', b'ERC-3009'), (b'ERC3023', b'ERC-3023'), (b'PHY120D', b'PHY-120D'), (b'PHY120E', b'PHY-120E')]),
            preserve_default=True,
        ),
    ]
