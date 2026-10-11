#!/usr/bin/env python3
"""Read-only stdlib checks of actual public output; no writes, network or science.

The manifest is an integrity inventory, not a signature. PDF page destinations
are checked against renderer metadata bound to PDF bytes, not independently
decoded by this script. Visual, scientific and publication acceptance are separate.
"""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import csv
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DISTRIBUTION_SIDECARS = {'downloads/complete-public-package.zip', 'downloads/SHA256SUMS'}
EXPECTED = json.loads((ROOT / "scripts/expected-content.public.json").read_text())

LIMITATIONS = [
    'This checks package integrity, retained content, declared routes and keyless arithmetic only.',
    'The manifest is not signed authenticity; coordinated edits to verifier and manifest are outside this integrity check.',
    'PDF page count/anchor metadata comes from the renderer and is bound to exact PDF bytes; PDF pages/bookmarks/text are not independently decoded here.',
    'HTML text checks inspect parsed non-hidden DOM text, not CSS layout, pixels, reading order or accessibility conformance.',
    'No visual acceptance, exhaustive confidentiality/security review, scientific certification or publication authorization is supplied.',
    'No secret-key membership, original generation, historical hardware/execution authentication, calibrated inference or complete exporter reproduction is performed.',
    'Static external-asset checks do not prove that arbitrary JavaScript can never access the network; runtime offline review is separate.',
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def strict_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON field in ' + path.name + ': ' + key)
            result[key] = value
        return result
    def number(text):
        value = float(text)
        require(math.isfinite(value), 'Nonfinite JSON number in ' + path.name)
        return value
    def invalid(value):
        raise ValueError('Nonfinite JSON constant in ' + path.name)
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs, parse_float=number, parse_constant=invalid)


def relative_file(value):
    require(isinstance(value, str) and bool(value), 'Missing relative filename')
    require(not PurePosixPath(value).is_absolute() and '\\' not in value and ':' not in value,
            'Unsafe relative filename: ' + value)
    require(not any(ord(c) < 32 or ord(c) == 127 for c in value), 'Control character in filename')
    require(all(x not in ('', '.', '..') for x in value.split('/')), 'Unsafe path component: ' + value)
    target = ROOT / value
    require(not ROOT.is_symlink(), 'Package root is a symlink')
    for part in [target, *target.parents]:
        if part == ROOT:
            break
        require(not part.is_symlink(), 'Symlink forbidden: ' + value)
    require(target.is_file(), 'Missing regular payload file: ' + value)
    return target


def json_file(name):
    return strict_json(relative_file(name))


def exact_ids(rows, expected, description):
    require(isinstance(rows, list) and all(isinstance(r, dict) for r in rows), 'Invalid records: ' + description)
    ids = [r['id'] for r in rows]
    require(len(ids) == len(set(ids)) and set(ids) == set(expected), 'ID conservation failed: ' + description)
    return {r['id']: r for r in rows}


def inventory_check():
    manifest = json_file('PUBLIC_MANIFEST.json')
    require(manifest['schema'] == 'axispl.public-product-manifest.v1', 'Unexpected output manifest schema')
    listed = {}
    for row in manifest['files']:
        name = row['path']
        require(name not in listed and name not in ('PUBLIC_MANIFEST.json', 'receipts/SHA256SUMS'), 'Duplicate/self-referential manifest entry')
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'Invalid payload byte count')
        require(isinstance(row['sha256'], str) and re.fullmatch('[0-9a-f]{64}', row['sha256']), 'Invalid SHA256 value')
        target = relative_file(name)
        require(digest(target) == row['sha256'] and target.stat().st_size == row['bytes'], 'Payload hash/size mismatch: ' + name)
        listed[name] = row['sha256']
    actual = set()
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(), 'Symlink forbidden anywhere in package')
        require(path.is_file() or path.is_dir(), 'Special filesystem member forbidden')
        if path.is_file():
            actual.add(path.relative_to(ROOT).as_posix())
    sidecars = actual & DISTRIBUTION_SIDECARS
    require(not sidecars or sidecars == DISTRIBUTION_SIDECARS, 'Incomplete distribution sidecars')
    require(actual == set(listed) | {'PUBLIC_MANIFEST.json', 'receipts/SHA256SUMS'} | sidecars, 'Exact allowlist inventory mismatch')
    sums = {}
    for line in relative_file('receipts/SHA256SUMS').read_text(encoding='utf-8').splitlines():
        require(bool(line), 'Empty checksum ledger line')
        expected, name = line.split('  ', 1)
        require(re.fullmatch('[0-9a-f]{64}', expected) and name not in sums, 'Invalid/duplicate checksum entry')
        require(digest(relative_file(name)) == expected, 'Checksum ledger mismatch: ' + name)
        sums[name] = expected
    require(set(sums) == set(listed) | {'PUBLIC_MANIFEST.json'}, 'Checksum ledger coverage mismatch')
    for name in actual:
        if name.endswith('.json'):
            json_file(name)
    if sidecars:
        archive = relative_file('downloads/complete-public-package.zip')
        ledger = relative_file('downloads/SHA256SUMS').read_text().strip()
        require(ledger == digest(archive) + '  complete-public-package.zip', 'Archive checksum mismatch')
        with zipfile.ZipFile(archive) as zipped:
            names = zipped.namelist()
            prefix = manifest['candidate'] + '/'
            required = set(listed) | {'PUBLIC_MANIFEST.json', 'receipts/SHA256SUMS'}
            require(len(names) == len(set(names)) and set(names) == {prefix + n for n in required}, 'Archive payload inventory differs')
            for member in zipped.infolist():
                require(not member.flag_bits & 1 and member.file_size <= 32 * 1024**2, 'Unexpected archive member')
                name = member.filename.removeprefix(prefix)
                require(hashlib.sha256(zipped.read(member)).hexdigest() == digest(relative_file(name)), 'Archive bytes differ: ' + name)
    return listed


def source_check():
    data = {}
    for name, spec in EXPECTED['groups'].items():
        rows = json_file(spec['path'])[spec['key']]
        mapping = exact_ids(rows, spec['ids'], name)
        for id_, record in mapping.items():
            fields = spec['fields'][id_]
            require(all(k in record for k in fields), 'Source field lost: ' + id_)
            retained = {k: record[k] for k in fields}
            require(object_digest(retained) == spec['hashes'][id_], 'Preserved source content changed: ' + id_)
        data[name] = mapping
    records, questions = data['research'], data['questions']
    forward = {(r['id'], q) for r in records.values() for q in r['related_existing_ids']}
    backward = {(r, q['id']) for q in questions.values() for r in q['related_research_records']}
    require(forward == backward and all(r in records and q in questions for r, q in forward), 'Bidirectional R/question routes differ')
    require({r for r,q in forward if q == 'A-05'} == {'R16'}, 'A-05 separate R16 route lost')
    require(records['R16']['later_related_episode']['question_id'] == 'A-05', 'R16 later episode lost')
    content = json_file('data/content-map.public.json')
    for key, group in [('research_records','research'), ('questions','questions'), ('gates','gates')]:
        exact_ids(content[key], data[group], 'content map ' + key)
    require({(r['id'], q) for r in content['research_records'] for q in r['question_ids']} == forward, 'Content map forward routes differ')
    require({(r, q['id']) for q in content['questions'] for r in q['research_records']} == forward, 'Content map reverse routes differ')
    for source in data['sources'].values():
        for name in source['included_derivatives']:
            relative_file(name)
    def source_refs(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'source_ids':
                    require(set(value) <= set(data['sources']), 'Unknown source ID')
                source_refs(value)
        elif isinstance(obj, list):
            for value in obj:
                source_refs(value)
    for group in data.values():
        source_refs(group)
    require(all(not any('gate' in key.lower() for key in c) for c in data['claims'].values()), 'Unsourced direct claim-to-gate field added')
    return data


def arithmetic_check():
    profile = json_file('fixtures/profile.public.json')
    require(object_digest(profile) == EXPECTED['profile_hash'], 'Profile identity changed')
    width, vocab = profile['context_width'], profile['vocabulary_size']
    require(type(width) is int and width == 4 and type(vocab) is int and vocab == 151936, 'Unexpected profile bounds')
    require(profile['excluded_target_ids'] == [151643,151646] and profile['gamma'] == .25 and profile['historical_minimum_scorable_tokens'] == 100, 'Profile exclusions/eligibility changed')
    counts, track = {}, []
    for sample in ('clean','marked'):
        fixture = json_file('fixtures/' + sample + '-completion.public.json')
        ids = fixture['completion_ids']
        require(fixture['sample'] == sample and len(ids) == 256 and object_digest(ids) == EXPECTED['completion_hashes'][sample], 'Completion identity changed')
        require(all(type(i) is int and 0 <= i < vocab for i in ids), 'Invalid completion token ID')
        contexts, windows, eligible = set(), set(), 0
        for i, target in enumerate(ids):
            if i < width:
                wc = cc = 'unscored_prefix'
            elif target in profile['excluded_target_ids']:
                wc = cc = 'excluded_target'
            else:
                eligible += 1
                context = tuple(ids[i-width:i]); window = context + (target,)
                wc = 'first_window' if window not in windows else 'repeated_window'
                cc = 'first_context' if context not in contexts else 'repeated_context'
                contexts.add(context); windows.add(window)
            track.append({'sample':sample, 'position_zero_based':i, 'window_class':wc, 'context_class':cc})
        counts[sample] = {'eligible_positions':eligible, 'distinct_contexts':len(contexts), 'distinct_windows':len(windows)}
    require(counts == {'clean':{'eligible_positions':252,'distinct_contexts':249,'distinct_windows':251},'marked':{'eligible_positions':252,'distinct_contexts':93,'distinct_windows':93}}, 'Unexpected trace counts')
    require(len(track) == 512 and json_file('data/observation-tracks.public.json')['rows'] == track, '512-row recurrence track differs from retained IDs')
    results = json_file('data/results.public.json')
    require(results['generated_pairs'] == 1 and type(results['generated_pairs']) is int and results['statistical_calibration_qualified'] is False, 'Result scope changed')
    require(results['computed_utc'] == '2026-10-07T23:26:27.485292+00:00' and results['return_review_date'] == '2026-10-08', 'Computation/review chronology changed')
    rows = results['rows']
    require(len(rows) == 18 and object_digest(rows) == EXPECTED['result_rows_hash'], 'Retained 18 result rows changed')
    count_fields = {'raw_positions':'eligible_positions','first_context':'distinct_contexts','first_window':'distinct_windows'}
    identities = set()
    for row in rows:
        key = (row['sample'], row['key_role'], row['unit'])
        require(key not in identities, 'Duplicate numeric row'); identities.add(key)
        h,n,gamma,z = row['hits'], row['denominator'], row['gamma'], row['nominal_z']
        require(type(h) is int and type(n) is int and 0 <= h <= n, 'Invalid supplied aggregate')
        require(n == counts[row['sample']][count_fields[row['unit']]] and gamma == .25, 'Unit/profile mismatch')
        require(math.isfinite(z) and math.isclose((h-n*gamma)/math.sqrt(n*gamma*(1-gamma)), z, rel_tol=1e-12, abs_tol=1e-12), 'Nominal score arithmetic mismatch')
    require(identities == {(s,k,u) for s in ('clean','marked') for k in ('primary','wrong_key_1','wrong_key_2') for u in count_fields}, 'Incomplete sample/key/unit matrix')
    with relative_file('data/results.public.csv').open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames is not None and len(reader.fieldnames) == len(set(reader.fieldnames)) and set(reader.fieldnames) == set(rows[0]), 'CSV field mismatch')
        csvrows = list(reader)
    require(len(csvrows) == len(rows), 'CSV row count mismatch')
    for a,b in zip(csvrows,rows):
        require(set(a) == set(b) and all(a[k] == str(v) for k,v in b.items()), 'CSV/JSON row mismatch')
    actual = {'schema':'axispl.design-keyless-check.v1','sample_counts':counts,'score_arithmetic_rows':18,'membership_measured':False,'new_generation':False,'historical_device_execution_authenticated':False}
    require(canonical(json_file('data/keyless-check.expected.json')) == canonical(actual), 'Keyless expected-output mismatch')
    observer = json_file('data/observer-receipt.public.json')
    require(observer['counts'] == counts and observer['historical_score_arithmetic_checks'] == 6 and observer['models_or_secret_keys_used_by_reported_observer'] is False, 'Observer scientific scope changed')
    require(observer['reproduction_command'] == 'python3 scripts/verify_public_package.py' and observer['expected_output'] == 'data/keyless-check.expected.json', 'Observer command does not address actual public verifier')
    require(observer['limitations'] == EXPECTED['observer_limitations'] and observer['reported_outcome'] == EXPECTED['observer_outcome'], 'Observer expected-output/peer-report caveats changed')
    return actual


def normalize(value):
    text = re.sub('[\u2010-\u2015\u2212]', '-', str(value))
    text = re.sub(r'\s*-\s*', '-', text)
    return ' '.join(text.split())


class HTMLContent(HTMLParser):
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, name):
        super().__init__(convert_charrefs=True)
        self.name=name; self.stack=[]; self.ids={}; self.tags={}; self.refs=[]; self.all_text=[]
    def handle_starttag(self, tag, attrs):
        keys=[k for k,v in attrs]
        require(len(keys)==len(set(keys)), 'Duplicate HTML attribute: '+self.name)
        a=dict(attrs)
        require(tag!='base','HTML base element would change package-relative routes')
        hidden=bool(self.stack and self.stack[-1][2]) or tag in ('script','style') or 'hidden' in a or a.get('aria-hidden','').lower()=='true'
        id_=a.get('id')
        if id_ is not None:
            require(bool(id_) and id_ not in self.ids,'Duplicate/empty HTML anchor: '+str(id_))
            self.ids[id_]=[];self.tags[id_]=tag
        if tag not in self.VOID:self.stack.append((tag,id_,hidden))
        for key in ('href','src','poster','data','action'):
            if a.get(key):self.refs.append((a[key], tag=='a' and key=='href'))
        if a.get('srcset'):
            for item in a['srcset'].split(','):
                require(bool(item.strip()),'Empty srcset candidate')
                self.refs.append((item.strip().split()[0],False))
        if tag=='meta':require(a.get('http-equiv','').lower()!='refresh','Automatic meta refresh forbidden')
        if 'style' in a:
            self.refs.extend((u,False) for u in css_urls(a['style']))
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)
        if tag not in self.VOID:self.handle_endtag(tag)
    def handle_endtag(self, tag):
        if tag in self.VOID:return
        require(bool(self.stack) and self.stack[-1][0]==tag,'Unbalanced HTML structure at </'+tag+'> in '+self.name)
        self.stack.pop()
    def handle_data(self, value):
        if self.stack and self.stack[-1][0]=='style':
            self.refs.extend((u,False) for u in css_urls(value))
        if self.stack and self.stack[-1][2]:return
        self.all_text.append(value)
        for tag,id_,hidden in self.stack:
            if id_ is not None and not hidden:self.ids[id_].append(value)
    def finish(self):
        self.close();require(not self.stack,'Unclosed HTML structure: '+self.name)
        self.ids={k:normalize(' '.join(v)) for k,v in self.ids.items()}
        self.all_text=normalize(' '.join(self.all_text))


def css_urls(text):
    require('\\' not in text or not re.search(r'(?:url|import)\s*\\',text,re.I),'Escaped CSS resource syntax requires manual review')
    urls=[m.group(2).strip() for m in re.finditer(r'url\(\s*([\'\"]?)(.*?)\1\s*\)',text,re.I|re.S)]
    urls += [m.group(2) for m in re.finditer(r'@import\s+([\'\"])(.*?)\1',text,re.I|re.S)]
    return urls


def resolve_reference(owner, value, allow_external, htmls):
    parsed=urlsplit(value)
    if parsed.scheme or parsed.netloc:
        require(allow_external and parsed.scheme in ('http','https') and bool(parsed.netloc),'Automatic or unsupported external reference in '+owner+': '+value)
        return
    require(not parsed.query,'Local query route not supported: '+value)
    decoded=unquote(parsed.path)
    require('\\' not in decoded and '\x00' not in decoded and not decoded.startswith('/'),'Unsafe local reference: '+value)
    target=((ROOT/owner).parent/decoded).resolve() if decoded else (ROOT/owner).resolve()
    require(target.is_relative_to(ROOT.resolve()),'Reference escapes package: '+value)
    name=target.relative_to(ROOT.resolve()).as_posix()
    if name in DISTRIBUTION_SIDECARS and not target.exists():
        return
    relative_file(name)
    if parsed.fragment:
        fragment=unquote(parsed.fragment)
        if name in htmls:require(fragment in htmls[name].ids,'Broken HTML fragment: '+owner+' → '+value)
        elif name.endswith('.svg'):
            root=ET.parse(target).getroot();require(fragment in {e.get('id') for e in root.iter()},'Broken SVG fragment: '+value)
        elif name.endswith('.pdf'):
            require(bool(re.fullmatch(r'page=[1-9][0-9]*',fragment)),'Unsupported PDF fragment: '+value)
        else:raise ValueError('Unverifiable fragment target: '+value)


def strings(value, omit_keys=()):
    if isinstance(value,str):
        if value.strip():yield value
    elif isinstance(value,dict):
        for key,item in value.items():
            if key not in omit_keys:yield from strings(item,omit_keys)
    elif isinstance(value,list):
        for item in value:yield from strings(item,omit_keys)


def contains(text, value, context):
    require(normalize(value) in text,'Substantive text absent in '+context+': '+str(value)[:120])


def html_check(data, listed):
    htmls={}
    for name in ('index.html','report/report.html'):
        document=HTMLContent(name);document.feed(relative_file(name).read_text(encoding='utf-8'));document.finish();htmls[name]=document
        require(not re.search(r'\[\s*FIGURE\s*:',document.all_text,re.I),'Unresolved figure placeholder in '+name)
        for group in data.values():
            for id_ in group:require(id_ in document.ids and document.tags[id_]=='article','Missing substantive article '+id_+' in '+name)
        for id_,r in data['research'].items():
            body=document.ids[id_]
            for field in ('title','observation','assumptions','alternative_explanations','claim_ceiling','next_discriminator','novelty_status','epistemic_status','signal_state','retention_requirement'):
                contains(body,r[field],name+'#'+id_+'/'+field)
            for field in ('source_availability','public_abstraction','reopening_condition'):
                contains(document.all_text,r[field],name+'/'+id_+'/'+field)
            if id_ in ('R39','R40'):contains(body,r['public_abstraction'],name+'#'+id_+'/abstraction')
            if 'later_related_episode' in r:
                for value in strings(r['later_related_episode']):contains(body,value,name+'#R16/later episode')
        for id_,q in data['questions'].items():
            body=document.ids[id_];contains(body,q['question_or_probe'],name+'#'+id_)
            for value in strings(q['effective_disposition'],('layer','stage')):contains(body,value,name+'#'+id_+'/effective')
            for history in q['historical_records']:
                for value in strings(history['record']):contains(body,value,name+'#'+id_+'/history')
            for value in strings(q['additive_status_history'],('layer','stage')):contains(body,value,name+'#'+id_+'/additive')
            for field in ('publication_custody_update','publication_scope_note','computation_date','return_review_date'):
                if field in q:
                    for value in strings(q[field]):contains(body,value,name+'#'+id_+'/'+field)
        for id_,g in data['gates'].items():
            for field in ('original_question','current_evidence_reported','required_action_or_disposition_reported'):contains(document.ids[id_],g[field],name+'#'+id_+'/'+field)
        for id_,claim in data['claims'].items():
            for field in ('claim','status','limit','public_reproduction'):contains(document.ids[id_],claim[field],name+'#'+id_+'/'+field)
            for field in ('status_scope','reopening_condition'):
                shared=claim[field]==next(iter(data['claims'].values()))[field]
                contains(document.ids['claim-common-rule'] if shared else document.ids[id_],claim[field],name+'#'+id_+'/'+field)
            contains(document.ids[id_],'Shared status and reopening rule',name+'#'+id_+'/common rule route')
        for id_,source in data['sources'].items():
            for field in ('title','origin','availability','verification_ceiling'):contains(document.ids[id_],source[field],name+'#'+id_+'/'+field)
        for id_,c in data['contributions'].items():
            for field in ('contribution','planning_disposition','local_reason'):contains(document.ids[id_],c[field],name+'#'+id_+'/'+field)
            if c['reopening_trigger']:contains(document.ids[id_],c['reopening_trigger'],name+'#'+id_+'/trigger')
        for id_,c in data['formats'].items():
            for field in ('adapted_name','status','reader_question','semantic_limit'):
                value=c[field]
                # Reviewed display-only spacing amendment; source fingerprints
                # still require the unchanged original C19 record.
                if id_=='C19' and field=='semantic_limit':value=value.replace('sum to100%', 'sum to 100%')
                contains(document.ids[id_],value,name+'#'+id_+'/'+field)
        require('result-table' in document.ids,'Missing searchable numeric table')
        for row in json_file('data/results.public.json')['rows']:
            contains(document.all_text,str(row['hits'])+'/'+str(row['denominator']),name+'/numeric table')
            contains(document.all_text,format(row['nominal_z'],'.4f'),name+'/numeric table')
        for fid in ['fig-F'+str(i).zfill(2) for i in range(1,11)]:
            require(fid in document.ids and document.tags[fid]=='figure' and len(document.ids[fid])>50,'Missing/empty figure '+fid)
    for name in ('evidence.html','pdf.html'):
        document=HTMLContent(name);document.feed(relative_file(name).read_text(encoding='utf-8'));document.finish();htmls[name]=document
    for name,doc in htmls.items():
        for value,external in doc.refs:resolve_reference(name,value,external,htmls)
    for name in listed:
        if name.endswith('.css'):
            for value in css_urls(relative_file(name).read_text(encoding='utf-8')):resolve_reference(name,value,False,htmls)
        if name.endswith('.svg'):
            raw=relative_file(name).read_text(encoding='utf-8')
            require(not re.search(r'<!ENTITY',raw,re.I),'SVG custom entity declarations forbidden')
            # ElementTree does not fetch the standard Matplotlib SVG DTD. Permit
            # only this fixed declaration, with no custom/internal subset.
            declarations=re.findall(r'<!DOCTYPE[^>]*>',raw,re.I|re.S)
            require(all(re.fullmatch(r'<!DOCTYPE\s+svg\s+PUBLIC\s+"-//W3C//DTD SVG 1\.1//EN"\s+"http://www\.w3\.org/Graphics/SVG/1\.1/DTD/svg11\.dtd"\s*>',d) for d in declarations),'Unexpected SVG document type declaration')
            root=ET.fromstring(raw)
            require(root.tag.split('}')[-1]=='svg','SVG root element missing')
            for element in root.iter():
                tag=element.tag.split('}')[-1].lower()
                require(tag not in ('script','foreignobject'),'Active SVG content forbidden: '+name)
                for key,value in element.attrib.items():
                    local=key.split('}')[-1].lower()
                    require(not local.startswith('on'),'SVG event handler forbidden')
                    if local in ('href','src'):resolve_reference(name,value,False,htmls)
                    if local=='style':
                        for url in css_urls(value):resolve_reference(name,url,False,htmls)
                if tag=='style' and element.text:
                    for url in css_urls(element.text):resolve_reference(name,url,False,htmls)
    return htmls


def implementation_check(data,htmls):
    for path,group in [('data/contribution-implementation.public.json','contributions'),('data/format-implementation.public.json','formats')]:
        rows=json_file(path)['decisions'];mapping=exact_ids(rows,data[group],path)
        for id_,row in mapping.items():
            require(all(row.get(k) and isinstance(row[k],(str,list,dict)) for k in ('disposition','reason','evidence')),'Missing implementation disposition/reason/evidence: '+id_)
            require(row['disposition'] in ('incorporated','amended','deferred','excluded','adopted','adapted','not_selected','selected','used','not_used','retained_not_used','not_adopted','adapted_to_document','deferred_quantitative','implemented','implemented_with_scope','pending_candidate_check'),'Unknown implementation disposition: '+id_)
            if group=='contributions':
                require(row.get('planning_disposition')==data[group][id_]['planning_disposition'],'Preserved planning disposition missing/changed: '+id_)
                require(row['reason']==data[group][id_]['local_reason'],'Preserved planning reason changed: '+id_)
                if data[group][id_]['planning_disposition'] in ('deferred','excluded'):
                    require(row['disposition']==data[group][id_]['planning_disposition'],'Deferred/excluded contribution promoted: '+id_)
            for name in ('index.html','report/report.html'):
                doc=htmls[name]
                contains(doc.ids[id_],row['disposition'],name+'#'+id_+'/implementation')
                field='evidence' if group=='contributions' else 'reason'
                for value in strings(row[field]):contains(doc.ids[id_],value,name+'#'+id_+'/'+field)


def coverage_check(data,htmls):
    cov=json_file('coverage.json')
    require(cov['schema']=='axispl.actual-product-coverage.v1','Unexpected coverage schema')
    require(cov['candidate']=='Vitreos_AxisPL_Evidence_Atlas_20261011_purpose_context','Stale candidate coverage')
    require(cov['supplement']['source']=='manuscript/evidence.md' and 'A08' in cov['rendered_anchors'],'Missing evidence supplement coverage')
    groups=json_file('data/artifact-catalog.public.json')['groups']
    group_destinations=exact_ids(cov['artifact_groups'],[g['id'] for g in groups],'artifact destinations')
    for id_,destination in group_destinations.items():
        require(destination['pdf_page']==cov['rendered_anchors'][id_]['page'],'Artifact PDF destination mismatch')
        require(destination['html_anchor']=='index.html#'+id_ and destination['catalog_anchor']=='evidence.html#'+id_,'Artifact HTML destination mismatch')
        require(all(id_ in htmls[name].ids for name in ('index.html','report/report.html','evidence.html')),'Missing artifact group anchor')
    pdf=relative_file(cov['pdf']);require(pdf.suffix=='.pdf' and pdf.read_bytes().startswith(b'%PDF-'),'Missing PDF signature')
    require(digest(pdf)==cov['pdf_sha256'],'Coverage does not bind current PDF bytes')
    pages=cov['pdf_pages'];require(type(pages) is int and pages>0,'Invalid renderer-reported page count')
    kind={'research':'research','questions':'question_probe','gates':'historical_gate','claims':'claim','contributions':'contribution','sources':'source','formats':'format_candidate'}
    expected={id_:(kind[group],EXPECTED['groups'][group]['path']) for group,records in data.items() for id_ in records}
    expected.update({'fig-F'+str(i).zfill(2):('figure','figures/figures.json') for i in range(1,11)})
    entries=exact_ids(cov['entries'],expected,'actual rendered coverage')
    anchors=cov['rendered_anchors'];require(isinstance(anchors,dict),'Missing renderer anchors')
    for id_,row in entries.items():
        require((row['kind'],row['source'])==expected[id_],'Coverage kind/source mismatch: '+id_)
        require(row['html_anchor']=='index.html#'+id_ and row['report_anchor']=='report/report.html#'+id_,'Coverage target mismatch: '+id_)
        page=row['pdf_page'];require(type(page) is int and 1<=page<=pages,'Invalid PDF destination: '+id_)
        require(id_ in anchors and anchors[id_]['page']==page,'Coverage/renderer page disagreement: '+id_)
        require(all(id_ in htmls[name].ids for name in ('index.html','report/report.html')),'Coverage anchor missing from HTML: '+id_)
        relative_file(row['source'])
    for id_,row in anchors.items():
        require(id_ in htmls['report/report.html'].ids and type(row['page']) is int and 1<=row['page']<=pages,'Invalid renderer anchor: '+id_)
        position=row['position_points'];require(isinstance(position,list) and len(position)==2 and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in position),'Invalid rendered anchor position')
    figs=json_file('figures/figures.json');figs=figs if isinstance(figs,list) else figs['figures']
    exact_ids(figs,['F'+str(i).zfill(2) for i in range(1,11)],'figure metadata')
    for figure in figs:
        require(all(figure.get(k) for k in ('title','description','caption','observation_unit','source_ids','record_ids','limits')),'Incomplete figure semantics')
        require(set(figure['source_ids'])<=set(data['sources']) and set(figure['record_ids'])<=set(data['research']),'Unknown figure source/record')
        name='figures/'+PurePosixPath(figure['svg']).name;relative_file(name)
    return cov


def main():
    require(bool(EXPECTED),'Verifier authoring constants not populated')
    listed=inventory_check();data=source_check();arithmetic=arithmetic_check()
    htmls=html_check(data,listed);implementation_check(data,htmls);coverage=coverage_check(data,htmls)
    print(json.dumps({'status':'pass_for_package_integrity_content_routes_and_keyless_arithmetic',
        'payload_files':len(listed),'manifest_sha256':digest(ROOT/'PUBLIC_MANIFEST.json'),
        'source_counts':{k:len(v) for k,v in data.items()},'coverage_entries':len(coverage['entries']),
        'pdf_sha256':coverage['pdf_sha256'],'renderer_reported_pdf_pages':coverage['pdf_pages'],
        'keyless_check':arithmetic,'limitations':LIMITATIONS},indent=2))


if __name__=='__main__':
    try:
        main()
    except (OSError,ValueError,KeyError,TypeError,AttributeError,IndexError,ET.ParseError) as exc:
        print(json.dumps({'status':'fail','error':str(exc)},indent=2),file=sys.stderr)
        raise SystemExit(1)
