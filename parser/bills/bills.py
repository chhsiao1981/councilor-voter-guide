#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import psycopg2
import json
import db_settings
import common


def Bill(bill):

    complement = {'type': '', 'category': '', 'abstract': '', 'last_action': '', 'proposed_by': '', 'committee': '', 'resolusion_date': '', 'resolusion_sitting': '', 'resolusion': '', 'bill_no': '', 'intray_date': '', 'intray_no': '', 'receipt_date': '', 'examination_date': '', 'examination': '', 'dispatch_no': '', 'dispatch_date': '', 'execution': '', 'remark': '', 'links': ''}
    complement.update(bill)
    complement['proposed_by'] = ' '.join(complement['proposed_by'])
    c.execute('''
        UPDATE bills_bills
        SET ad = %(ad)s, type = %(type)s, category = %(category)s, abstract = %(abstract)s, last_action = %(last_action)s, proposed_by = %(proposed_by)s, committee = %(committee)s, resolusion_date = %(resolusion_date)s, resolusion_sitting = %(resolusion_sitting)s, resolusion = %(resolusion)s, bill_no = %(bill_no)s, intray_date = %(intray_date)s, intray_no = %(intray_no)s, receipt_date = %(receipt_date)s, examination_date = %(examination_date)s, examination = %(examination)s, dispatch_no = %(dispatch_no)s, dispatch_date = %(dispatch_date)s, execution = %(execution)s, remark = %(remark)s, links = %(links)s
        WHERE uid = %(id)s and county = %(county)s
    ''', complement)
    c.execute('''
        INSERT into bills_bills(uid, ad, county, type, category, abstract, last_action, proposed_by, committee, resolusion_date, resolusion_sitting, resolusion, bill_no, intray_date, intray_no, receipt_date, examination_date, examination, dispatch_no, dispatch_date, execution, remark, links)
        SELECT %(id)s, %(ad)s, %(county)s, %(type)s, %(category)s, %(abstract)s, %(last_action)s, %(proposed_by)s, %(committee)s, %(resolusion_date)s, %(resolusion_sitting)s, %(resolusion)s, %(bill_no)s, %(intray_date)s, %(intray_no)s, %(receipt_date)s, %(examination_date)s, %(examination)s, %(dispatch_no)s, %(dispatch_date)s, %(execution)s, %(remark)s, %(links)s
        WHERE NOT EXISTS (SELECT 1 FROM bills_bills WHERE uid = %(id)s and county = %(county)s)
    ''', complement)

def CouncilorsBills(councilor_id, bill_id, priproposer, petition):
    c.execute('''
        INSERT into bills_councilors_bills(councilor_id, bill_id, priproposer, petition)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM bills_councilors_bills WHERE councilor_id = %s AND bill_id = %s)
    ''', (councilor_id, bill_id, priproposer, petition, councilor_id, bill_id))

conn = db_settings.con()
c = conn.cursor()
#dict_c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

ad = 11
county = u'臺北市'
dict_list = json.load(open('../../data/taipei/bills-%s.json' % str(ad)))
for bill in dict_list:
    if 1:   break
    bill.update({'ad': ad, 'county': county})
    Bill(bill)
    priproposer = True
    for name in bill['proposed_by']:
        councilor_id = common.getDetailId(c, name, ad, county)
        if councilor_id:
            CouncilorsBills(councilor_id, bill['id'], priproposer, None)
        priproposer = False
conn.commit()
print 'bills done'

import numpy as np


def bill_party_diversity():
    c.execute('''
        select
            b.bill_id,
            sum(case when a.party = '中國國民黨' then 1 else 0 end) KMT,
            sum(case when a.party = '民主進步黨' then 1 else 0 end) DDP,
            sum(case when a.party = '臺灣團結聯盟' then 1 else 0 end) TSU,
            sum(case when a.party = '親民黨' then 1 else 0 end) PFP,
            sum(case when a.party = '新黨' then 1 else 0 end) NP,
            sum(case when a.party = '無黨籍' then 1 else 0 end) N
        from councilors_councilorsdetail a, bills_councilors_bills b
        where a.id = b.councilor_id
        group by b.bill_id
    ''')
    for bill_diversity in c.fetchall():
        bill_diversity = list(bill_diversity)
        vector = np.array(bill_diversity[1:])
        normalized = vector / np.linalg.norm(vector)
        c.execute('''
            UPDATE bills_bills
            SET param = %s
            WHERE uid = %s
        ''', ({'diversity': list(normalized)}, bill_diversity[0]))

def personal_vector(councilor_id):
    c.execute('''
        SELECT a.param::json->'diversity'
        FROM bills_bills a, bills_councilors_bills b
        WHERE a.uid = b.bill_id AND b.councilor_id = %s
    ''', (councilor_id, ))
    r = c.fetchall()
    p_vector = list(np.sum([x[0] for x in r], axis=0) / float(len(r)))
    c.execute('''
        UPDATE councilors_councilorsdetail
        SET param = %s
        WHERE id = %s
    ''', ({'diversity': p_vector}, councilor_id))

def councilors(ad, county):
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE ad = %s AND county = %s
    ''', (ad, county))
    return c.fetchall()

bill_party_diversity()
for councilor_id in councilors(ad, county):
    personal_vector(councilor_id)
conn.commit()
