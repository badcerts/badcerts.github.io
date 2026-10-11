#!/usr/bin/env python3
"""Build the complete local atlas/report from explicit public inputs.

No network, model, secret key, scientific generation or publication operation.
The returned PDF and coverage are output artifacts, not input-packet checks.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlparse, unquote, quote
import posixpath
import argparse
import html
import json
import re
import shutil
import hashlib
import markdown

TITLE = 'Vitreos / AxisPL: AI Watermarking, Attribution and Provenance'
DAY = '11 October 2026'
CANDIDATE = 'Vitreos_AxisPL_Evidence_Atlas_20261011_purpose_context'
LABELS = {
    'epistemic_status':'Evidence origin / status', 'signal_state':'Observation / signal state',
    'alternative_explanations':'Alternative explanations', 'claim_ceiling':'Claim ceiling',
    'next_discriminator':'Next discriminator', 'novelty_status':'Novelty status',
    'retention_requirement':'Preservation requirement', 'public_abstraction':'Disclosed abstraction',
    'source_availability':'Source availability', 'reopening_condition':'Reopening condition',
    'next_step_execution_performed_by_this_review':'Next step executed by this review',
    'later_related_episode':'Separate later episode',
}

def e(value):
    return html.escape(str(value), quote=True)

def load(root, name):
    return json.loads((root/name).read_text())

def label(key):
    return LABELS.get(key, key.replace('_',' ').capitalize())

def norm(value):
    return value.replace('\u2011','-').replace('\u2013','-').replace('\u2014',' - ')

def text(value):
    return e(norm(str(value)))

def link(id_, extra=''):
    return f'<a href="#{e(id_)}" {extra}>{e(id_)}</a>'

def links(ids):
    return ' · '.join(link(i) for i in ids)

def para(value):
    return f'<p>{text(value)}</p>'

def field(key,value):
    return f'<div class="field"><h4>{e(label(key))}</h4>{value_html(value)}</div>'

def value_html(value):
    if isinstance(value,dict):
        return '<dl class="structured">'+''.join(f'<dt>{e(label(k))}</dt><dd>{value_html(v)}</dd>' for k,v in value.items())+'</dl>'
    if isinstance(value,list):
        return '<ul>'+''.join('<li>'+value_html(v)+'</li>' for v in value)+'</ul>'
    if value is None:
        return '<span class="muted">Not specified in this source.</span>'
    if isinstance(value,bool):
        return 'Yes' if value else 'No'
    return para(value)

def md(value):
    rendered = markdown.markdown(norm(value),extensions=['tables','fenced_code','footnotes','sane_lists'])
    return rendered.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')

def table(headings,rows,cls=''):
    return f'<div class="table-wrap"><table class="{cls}"><thead><tr>'+''.join('<th scope="col">'+e(h)+'</th>' for h in headings)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def section(id_,title,body,cls='chapter'):
    mark=f'<span class="section-id">{e(id_)}</span> ' if re.fullmatch(r'[SMA]\d\d',id_) else ''
    return f'<section id="{e(id_)}" class="{cls}"><h2>{mark}{e(title)}</h2>{body}</section>'

def result_table(data):
    rows=[]
    names={'raw_positions':'Raw eligible positions','first_context':'First exact context','first_window':'First exact context + target'}
    for r in data['rows']:
        role=r['key_role'].replace('_',' ')
        rows.append([text(r['sample']),text(role),text(names[r['unit']]),f"{r['hits']}/{r['denominator']}",f"{r['nominal_z']:.4f}"])
    return '<h3 id="result-table">All 18 reported score analyses</h3>'+para('One retained clean/marked pair, six sample/key roles, three observation units. Every score is nominal z, not calibrated. Wrong-key rows are diagnostic roles, not new generations or independent samples. Membership hits are supplied from the preserved key-holder result; the public route checks counts and arithmetic only.')+table(['Specimen','Key role','Observation unit','Hits / n','Nominal z'],rows,'numeric')+para('Source: S-RESULTS; data/results.public.json and data/results.public.csv. Computed 7 October 2026 at 23:26 UTC; return/review 8 October. The historical 100-position minimum remains profile metadata: the 93-window calculation is descriptive and does not qualify a new threshold.')

def figure_html(fig,prefix):
    fid=fig['id']; fn=Path(fig['svg']).name
    limits = fig['limits'] if isinstance(fig['limits'], str) else ' '.join(fig['limits'])
    return (
        f'<figure id="fig-{e(fid)}"><div class="figure-scroll">'
        f'<img src="{prefix}figures/{e(fn)}" alt="{e(fig["description"])}"/></div>'
        f'<a class="screen-only figure-open" href="{prefix}figures/{e(fn)}">Open full-size vector figure</a>'
        f'<figcaption><strong>Figure {e(fid.removeprefix("F"))}. {text(fig["title"])}</strong> '
        f'{text(fig["caption"])}<br/><span class="figure-source">Unit: {text(fig["observation_unit"])}. '
        f'Sources: {links(fig["source_ids"])}. Records: {links(fig["record_ids"])}.</span><br/>'
        f'<span class="figure-limit">Limit: {text(limits)}</span></figcaption></figure>'
    )

def site_shell(body, prefix='', page='reader', title=TITLE):
    routes = [('S01','Why AI watermarking matters'),('S02','Hypotheses and corrections'),('S03','Early observations'),('S04','Instruments and contracts'),('S05','Owned experiment'),('S06','Field work and limits'),('S07','Open research'),('M01','Methods and specimens'),('A01','42 research records'),('A02','Questions and histories'),('A03','64 original gates'),('A04','Claim ledger'),('A05','Sources and bibliography'),('A06','Contributions and formats'),('A07','Glossary and subject index'),('A08','Evidence and downloads')]
    local = '' if page == 'reader' else prefix+'index.html'
    contents = ''.join(f'<li><a href="{local}#{id_}"><span>{id_}</span> {e(label_)}</a></li>' for id_,label_ in routes)
    primary = ''.join(f'<a href="{prefix}{path}"'+(' aria-current="page"' if page==key else '')+f'>{name}</a>' for key,path,name in [('reader','index.html','Read'),('evidence','evidence.html','Evidence'),('pdf','pdf.html','PDF')])
    navigation = f'''<aside class="screen-nav"><a class="site-name" href="{prefix}index.html">Vitreos / AxisPL</a><p class="edition-label">EVIDENCE ATLAS · OCTOBER 2026</p><nav class="primary-nav" aria-label="Views">{primary}</nav><label class="theme-control" hidden for="theme">Appearance <select id="theme"><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option></select></label><details class="section-menu" open><summary>Contents</summary><nav aria-label="Research sections"><ol>{contents}</ol></nav></details><p class="nav-note">Public edition<br/>11 October 2026</p></aside>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Vitreos investigates AI watermarking, counter-watermarking, attribution and provenance: why source evidence matters, what our experiments found and what remains unresolved."><title>{e(title)}</title><link rel="stylesheet" href="{prefix}assets/atlas.css"><script defer src="{prefix}assets/atlas.js"></script></head><body><a class="skip-link" href="#main">Skip to content</a>{navigation}<main id="main" tabindex="-1">{body}</main></body></html>'''

def make_document(root,prefix,figs):
    records=load(root,'data/research-register.public.json')['records']
    questions=load(root,'data/future-work.public.json')['questions_and_probes']
    gates=load(root,'data/original-gates.public.json')['gates']
    claims=load(root,'data/claim-ledger.public.json')['claims']
    sources=load(root,'data/source-map.public.json')['sources']
    contribs=load(root,'data/contribution-decisions.public.json')['decisions']
    candidates=load(root,'design/format-candidates.public.json')['records']
    titles={r['id']:r['title'] for r in records}
    sections=load(root,'data/content-map.public.json')['sections']
    parts=[]
    parts.append(f'''<section class="cover" id="cover"><p class="eyebrow">EVIDENCE ATLAS · AUGUST–OCTOBER 2026</p><h1>Vitreos / AxisPL</h1><p class="cover-subtitle">AI watermarking,<br/>attribution and provenance</p><div class="cover-rule"></div><p class="cover-description">How can we recognize AI-generated material, trace its origins, and judge the evidence after it has been edited or republished? Vitreos investigates watermarks, counter-watermarking and the limits of detection through experiments whose methods, failures and open questions remain available to inspect.</p><p class="cover-audience">For technical researchers, operators and collaborators working on questions that matter to educators, editors and anyone evaluating source evidence.</p><p class="cover-edition">Research begun in mid-August 2026. Experimental record through 9 October; context and publication revision: {DAY}. Public edition.</p></section>''')
    route_rows=[['Researcher','S01 → S03–S06 → M01 → A01','Inspect units, assumptions, alternatives, limits and original record bodies.'],['Operator','S01 → S04 → M01 → S07','Check prerequisites, available reproduction, stop conditions and deliberately selected next work.'],['Collaborator','S01 → S02 → S07 → A01/A02','Follow corrections, source availability and the next discriminating observation.']]
    parts[0]=parts[0].replace('</section>',f'<div class="download-actions screen-only"><a class="button" href="#S01">Why this work matters</a><a href="{prefix}pdf.html">Read the PDF</a><a href="{prefix}report/Vitreos_AxisPL_Evidence_Atlas.pdf" download>Download PDF</a><a href="{prefix}evidence.html">Explore the evidence</a></div></section>')
    toc=[(s['id'],s['title']) for s in sections[:7]]+[('M01','Methods and public reproduction'),('A01','Complete research register'),('A02','Questions, histories and discovery probes'),('A03','Original 64 gate obligations'),('A04','Claim ledger and explicit exclusions'),('A05','Sources and dated bibliography'),('A06','Contribution and design decisions'),('A07','Glossary and subject index'),('A08','Evidence tables and downloadable artifacts')]
    nav='<ol class="contents-list">'+''.join(f'<li><a class="page-ref" href="#{i}"><span class="mono">{i}</span> {e(t)}</a></li>' for i,t in toc)+'</ol>'
    parts.append(section('contents','Contents and reading routes',para('The narrative and complete registers are one research product. Start with a route below, then use stable identifiers and linked page references to inspect the underlying record. Each route reaches the same evidence and claim limits.')+nav+table(['Reader','Route','Purpose'],[[e(c) for c in r] for r in route_rows])+para('Page references and PDF bookmarks address this exact rendering. Every R01–R42 entry is substantive. Questions F-01–F-24, subquestions A-01–A-06 and discovery probes U-01–U-06 preserve their historical wording and current disposition. Gate IDs identify historical obligations, not 64 newly passed tests.')+'<h3>Figures</h3><ol class="contents-list">'+''.join(f'<li><a class="page-ref" href="#fig-{f["id"]}">Figure {f["id"].removeprefix("F")}. {text(f["title"])}</a></li>' for f in figs)+'</ol>'))
    narrative=(root/'manuscript/narrative.md').read_text()
    chunks=re.split(r'^##\s+(S0[1-7])(?:\s*[-:|.]?\s+)(.+?)\s*$',narrative,flags=re.M)
    if len(chunks)!=22:
        raise ValueError('Narrative must contain exactly seven ## S01 ... ## S07 sections')
    used=set()
    for idx in range(1,len(chunks),3):
        sid,title,body=chunks[idx:idx+3]
        rendered=md(body)
        def slot(m):
            fid=m.group(1);fig=next(f for f in figs if f['id']==fid);used.add(fid)
            out=figure_html(fig,prefix)
            if fid=='F07':out+=result_table(load(root,'data/results.public.json'))
            return out
        rendered=re.sub(r'<p>\[FIGURE:\s*(F\d+)\]</p>',slot,rendered)
        parts.append(section(sid,norm(title),rendered))
    methods=(root/'manuscript/methods.md').read_text()
    methods=methods.replace('[NATIVE-SPECIMENS]',(root/'manuscript/native-specimens.md').read_text()).replace('PACKAGE/',prefix)
    methods=re.sub(r'^#{1,2} M01.*\n','',methods,count=1)
    method_html=re.sub(r'<p>\[FIGURE:\s*(F\d+)\]</p>',slot,md(methods))
    parts.append(section('M01','Methods and public reproduction',method_html))
    unused=[f for f in figs if f['id'] not in used]
    if unused:
        raise ValueError('Unplaced figures: '+','.join(f['id'] for f in unused))
    intro=para('This is the full 42-record research register, including original proposals, weak observations, inspected absences, unavailable evidence, unmeasured mechanisms, corrections and conditional results. Each field is retained from the explicitly public source derivative; the JSON supplies the same source record in machine-readable form.')
    intro+='<div id="research-source-rule">'+para(records[0]['source_availability'])+para('Shared disclosure: '+records[0]['public_abstraction'])+'</div>'+para('No new execution is selected by any of these 42 records. A next discriminator is a condition for deliberately reopening a question, not an automatic assignment. Where next discriminator and reopening condition are identical, the field is printed once under a combined label. All record IDs also link to their main narrative section and questions.')
    intro+=table(['Record','Research thread','Narrative'],[[f'<a class="page-ref" href="#{r["id"]}">{r["id"]}</a>',text(r['title']),link(r['main_section_id'])] for r in records])
    for r in records:
        body=f'<p class="record-meta">Narrative: {link(r["main_section_id"])} · Questions: {links(r["related_existing_ids"])}<br/>Sources: {links(r["source_ids"])}</p>'
        body+='<p class="record-meta"><a href="#research-source-rule">Shared source and disclosure rule</a> · <a href="#A08">Available evidence</a></p>'
        for key in ['epistemic_status','signal_state','observation','assumptions','alternative_explanations','claim_ceiling']:
            body+=field(key,r[key])
        body+='<div class="field"><h4>Next discriminator / reopening condition</h4>'+value_html(r['next_discriminator'])+'</div>'
        for key in ['novelty_status','retention_requirement']:
            body+=field(key,r[key])
        if 'later_related_episode' in r:body+=field('later_related_episode',r['later_related_episode'])
        if r['public_abstraction']!=records[0]['public_abstraction']:body+=field('public_abstraction',r['public_abstraction'])
        intro+=f'<article class="research-record" id="{r["id"]}"><h3><span class="record-id">{r["id"]}</span> {text(r["title"])}</h3>{body}</article>'
    parts.append(section('A01','Complete research register',intro))
    qbody=para('Current effective dispositions are shown first. Baseline records and later additive stages remain visible as history. Old pending text is not a present assignment. In U-02, the historical control-label mistake remains recorded; the corrected positive-versus-negative control statement governs current interpretation. No new experiment is selected by this index.')
    qbody+=table(['ID','Question / probe'],[[f'<a class="page-ref" href="#{q["id"]}">{q["id"]}</a>',text(q['question_or_probe'])] for q in questions])
    for q in questions:
        qb=para(q['question_or_probe'])+f'<p class="record-meta">Research: {links(q["related_research_records"])} · Sources: {links(q["source_ids"])}</p>'
        qb+='<div class="current-disposition"><h4>Current effective disposition</h4>'+value_html(q['effective_disposition'])+'</div>'
        for key in ['publication_custody_update','publication_scope_note','computation_date','return_review_date']:
            if key in q:qb+=field(key,q[key])
        qb+='<h4>Preserved historical records</h4>'
        for h in q['historical_records']:
            qb+=f'<div class="history"><p class="history-label">Historical stage: <code>{e(h["stage"])}</code></p>'+table(['Field','Historical value'],[[e(label(k)),value_html(v)] for k,v in h['record'].items()],'history-table')+'</div>'
        if q['additive_status_history']:
            qb+='<h4>Additive status history</h4>'+''.join('<div class="history">'+value_html(h)+'</div>' for h in q['additive_status_history'])
        qbody+=f'<article class="question-record" id="{q["id"]}"><h3>{q["id"]} <span class="muted">{text(q["kind"].replace("_"," "))}</span></h3>{qb}</article>'
    parts.append(section('A02','Questions, histories and discovery probes',qbody))
    gb=para(load(root,'data/original-gates.public.json')['wording_note'])+para(gates[0]['current_scope_note'])
    gb+=para('Every row below is a historical snapshot and was not recertified by the design packet or by printing it here. The original gate wording, reported evidence and requested disposition are preserved. Actual product checks are documented separately in the candidate validation receipt.')
    for group in dict.fromkeys(g['id'].split('-')[0] for g in gates):
        selected=[g for g in gates if g['id'].startswith(group+'-')]
        gb+=f'<h3 id="gates-{group}">{group} · {len(selected)} original obligations</h3>'
        for g in selected:
            gb+=f'<article class="gate" id="{g["id"]}"><h4>{g["id"]} · {text(g["original_question"])}</h4>'+table(['Historical field','Preserved statement'],[['Evidence reported',text(g['current_evidence_reported'])],['Required action / disposition reported',text(g['required_action_or_disposition_reported'])],['Source',links(g['source_ids'])]])+'</article>'
    parts.append(section('A03','Original 64 gate obligations',gb))
    cb=para('The ledger keeps supported bounded statements and explicitly excluded stronger statements together. An excluded statement is included so that the boundary is inspectable; it is not a result. Source IDs here do not imply direct claim-to-question or claim-to-gate links.')
    cb+='<div id="claim-common-rule"><h3>Shared status and reopening rule</h3>'+field('status_scope',claims[0]['status_scope'])+field('reopening_condition',claims[0]['reopening_condition'])+'</div>'
    for c in claims:
        excluded=c['status'].startswith('excluded')
        cb+=f'<article class="claim {"excluded" if excluded else ""}" id="{c["id"]}"><h3>{c["id"]} · {text(c["status"])}</h3>'+field('claim',c['claim'])+field('limit',c['limit'])+field('public_reproduction',c['public_reproduction'])
        for key in ('status_scope','reopening_condition'):
            if c[key]!=claims[0][key]:cb+=field(key,c[key])
        cb+='<p class="record-meta"><a href="#claim-common-rule">Shared status and reopening rule</a></p>'+f'<p>Sources: {links(c["source_ids"])}</p></article>'
    parts.append(section('A04','Claim ledger and explicit exclusions',cb))
    sb=para('A public derivative route is not an independent original. Private and unavailable originals remain explicitly unavailable. No public reader is expected to reconstruct a local path or request undisclosed credentials. All included file routes below are relative to this package.')
    for s in sources:
        sb+=f'<article class="source-record" id="{s["id"]}"><h3>{s["id"]} · {text(s["title"])}</h3>'+''.join(field(k,s[k]) for k in ['origin','availability','verification_ceiling'])+'<p>Included derivative files:</p><ul>'+''.join(f'<li><a href="{prefix}{e(path)}"><code>{e(path)}</code></a></li>' for path in s['included_derivatives'])+'</ul></article>'
    background=(root/'manuscript/background-sources.md').read_text()
    background=re.sub(r'^# .*\n','',background,count=1)
    sb+='<h3 id="bibliography">Dated external bibliography</h3>'+md(background)
    sb+= '<h3 id="observer-receipt">Reported keyless observer</h3>'+value_html(load(root,'data/observer-receipt.public.json'))
    parts.append(section('A05','Sources and dated bibliography',sb))
    db=para('Reviewers and implementers worked from shared artifacts. Local implementation/key-holder work, field execution reports, research/context review, independent arithmetic review and editorial integration are distinct contributions. Multiple reviews do not create independent generations, keys, observations or institutional provenance.')+para('The original planning disposition and reason below are preserved as history. Candidate implementation evidence is a separate statement about this edition. In particular, historical descriptions of then-unbuilt pages do not describe the current rendering.')
    implementation=load(root,'data/contribution-implementation.public.json')['decisions']
    impl={c['id']:c for c in implementation}
    for c in contribs:
        d=impl[c['id']]
        db+=f'<article class="decision" id="{c["id"]}"><h3>{c["id"]} · {text(c["planning_disposition"])}</h3>'+para(c['contribution'])+field('planning_reason',c['local_reason'])+field('candidate_disposition',d['disposition'])+field('implementation_evidence',d['evidence'])
        if c['reopening_trigger'] is not None:db+=field('reopening_trigger',c['reopening_trigger'])
        db+='</article>'
    db+='<h3 id="design-decisions">Analytical-format selection</h3>'+para('The original decks supplied candidate explanatory formats, not measured data. These twenty candidate identities remain distinct from the figures selected for this report. Format selection changes presentation, not source claims.')
    decisions=load(root,'data/format-implementation.public.json')['decisions']
    dmap={d['id']:d for d in decisions}
    for c in candidates:
        d=dmap[c['id']]
        semantic_limit=c['semantic_limit']
        # Display-only spacing correction; the original C19 JSON is preserved.
        if c['id']=='C19':semantic_limit=semantic_limit.replace('sum to100%', 'sum to 100%')
        db+=f'<article class="design-decision" id="{c["id"]}"><h4>{c["id"]} · {text(c["adapted_name"])}</h4>'+table(['Field','Design disposition'],[['Original candidate status',text(c['status'])],['Source formats',text(', '.join(c['source_formats']))],['Reader question',text(c['reader_question'])],['Selected disposition',text(d['disposition'])],['Reason / evidence',text(d['reason'])],['Original semantic limit',text(semantic_limit)]])+'</article>'
    parts.append(section('A06','Contribution and design decisions',db))
    glossary=load(root,'data/glossary.public.json')['terms']
    gl=para('Definitions here fix the meaning used by this report. The subject index points to substantive records; it does not imply that every listed concept was measured or qualified.')
    for g in glossary:
        gl+=f'<article class="glossary-entry"><h3>{text(g["term"])}</h3>{para(g["definition"])}<p class="index-links">{links(g["records"])}</p></article>'
    gl+='<h3 id="subject-index">Subject index</h3>'+table(['Subject','Record destinations'],[[text(g['term']),' · '.join(f'<a class="page-ref" href="#{rid}">{rid}</a>' for rid in g['records'])] for g in sorted(glossary,key=lambda g:g['term'].lower())])
    parts.append(section('A07','Glossary and subject index',gl))
    supplement=(root/'manuscript/evidence.md').read_text().replace('PACKAGE/',prefix)
    supplement=re.sub(r'^## A08.*\n','',supplement,count=1)
    parts.append(section('A08','Evidence tables and downloadable artifacts',md(supplement)))
    main='\n'.join(parts)
    return site_shell(main,prefix)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--no-pdf',action='store_true');args=parser.parse_args();root=args.root.resolve()
    figures=load(root,'figures/figures.json')
    figs=figures if isinstance(figures,list) else figures['figures']
    assert len({f['id'] for f in figs})==len(figs)
    (root/'index.html').write_text(make_document(root,'',figs))
    (root/'report/report.html').write_text(make_document(root,'../',figs))
    evidence=(root/'manuscript/evidence.md').read_text().replace('PACKAGE/','')
    evidence=re.sub(r'^## A08.*\n','',evidence,count=1)
    evidence=re.sub(r'\]\(#((?!E\d\d)[^)]*)\)',r'](index.html#\1)',evidence)
    evidence_intro='<header class="view-heading"><p class="eyebrow">INSPECT · REPRODUCE · EXTEND</p><h1>Evidence and artifacts</h1><p>The report, exact specimens, full records, reusable figures and focused reproduction sources belong to one research product.</p><div class="download-actions"><a class="button" href="downloads/complete-public-package.zip" download>Download complete package</a><a href="docs/REPRODUCE.md">Reproduction guide</a><a href="docs/DATA_DICTIONARY.md">Data dictionary</a></div></header>'
    (root/'evidence.html').write_text(site_shell(evidence_intro+'<h2>Measurements and methods</h2>'+md(evidence),page='evidence',title='Evidence and artifacts · Vitreos / AxisPL'))
    pdf_path='report/Vitreos_AxisPL_Evidence_Atlas.pdf'
    pdf_body=f'''<header class="view-heading"><p class="eyebrow">THE COMPLETE RESEARCH RECORD</p><h1>Read the report</h1><p>The PDF includes the narrative, analytical figures, full registers, methods and evidence supplement. The HTML reader offers the same content with responsive navigation.</p><div class="download-actions"><a class="button" href="{pdf_path}">Open PDF</a><a href="{pdf_path}" download>Download PDF</a><a href="index.html">Read HTML</a><a href="evidence.html">Evidence and source files</a></div></header><object class="pdf-viewer" data="{pdf_path}" type="application/pdf" title="Vitreos / AxisPL Evidence Atlas"><p>This browser does not display the embedded PDF. <a href="{pdf_path}">Open the PDF</a> or <a href="index.html">read the complete HTML edition</a>.</p></object><p class="muted">The browser controls the PDF viewer and whether a download opens or saves. The links above remain available independently.</p>'''
    (root/'pdf.html').write_text(site_shell(pdf_body,page='pdf',title='Report PDF · Vitreos / AxisPL'))
    if args.no_pdf:return
    from weasyprint import HTML, default_url_fetcher
    from weasyprint.text.fonts import FontConfiguration
    def local_fetch(url,**kwargs):
        parsed=urlparse(url)
        if parsed.scheme!='file':raise ValueError('Automatic external request denied: '+parsed.scheme)
        path=Path(unquote(parsed.path)).resolve()
        if not path.is_relative_to(root):raise ValueError('Asset outside public root')
        return default_url_fetcher(url,**kwargs)
    document=HTML(filename=str(root/'report/report.html'),url_fetcher=local_fetch).render(font_config=FontConfiguration())
    # WeasyPrint resolves document links against the absolute authoring path.
    # Keep supplement links portable and exclude that private path from PDF
    # annotations (including tagged annotation Contents) before serialization.
    for page in document.pages:
        portable_links=[]
        for kind,target,rectangle,box in page.links:
            if kind=='external' and urlparse(target).scheme=='file':
                parsed=urlparse(target)
                path=Path(unquote(parsed.path)).resolve()
                if parsed.netloc or not path.is_relative_to(root) or not path.is_file():
                    raise ValueError('PDF supplement link outside public package')
                target=quote(posixpath.relpath(path.relative_to(root).as_posix(),'report'),safe='/')
                if parsed.fragment:target+='#'+parsed.fragment
            portable_links.append((kind,target,rectangle,box))
        page.links[:]=portable_links
    # Replace the file only after serialization; viewers may still hold the prior PDF open.
    pdf_output=root/'report/Vitreos_AxisPL_Evidence_Atlas.pdf'
    pdf_pending=pdf_output.with_suffix('.pdf.pending')
    try:
        document.write_pdf(pdf_pending,pdf_tags=True)
    except TypeError:
        document.write_pdf(pdf_pending)
    pdf_pending.replace(pdf_output)
    anchors={}
    for page_no,page in enumerate(document.pages,1):
        for id_,pos in page.anchors.items():
            # Renderer anchor rectangles use CSS pixels; expose their top-left
            # point in PDF points, with a top-left page origin.
            if id_ not in anchors:anchors[id_]={'page':page_no,'position_points':[float(v)*72/96 for v in pos[:2]]}
    rows=[]
    for fn,key,kind in [('research-register.public.json','records','research'),('future-work.public.json','questions_and_probes','question_probe'),('original-gates.public.json','gates','historical_gate'),('claim-ledger.public.json','claims','claim'),('contribution-decisions.public.json','decisions','contribution'),('source-map.public.json','sources','source')]:
        for r in load(root,'data/'+fn)[key]:
            id_=r['id'];assert id_ in anchors, id_
            rows.append({'id':id_,'kind':kind,'html_anchor':'index.html#'+id_,'report_anchor':'report/report.html#'+id_,'pdf_page':anchors[id_]['page'],'source':'data/'+fn})
    for c in load(root,'design/format-candidates.public.json')['records']:
        id_=c['id'];assert id_ in anchors,id_;rows.append({'id':id_,'kind':'format_candidate','html_anchor':'index.html#'+id_,'report_anchor':'report/report.html#'+id_,'pdf_page':anchors[id_]['page'],'source':'design/format-candidates.public.json'})
    for f in figs:
        id_='fig-'+f['id'];assert id_ in anchors,id_;rows.append({'id':id_,'kind':'figure','html_anchor':'index.html#'+id_,'report_anchor':'report/report.html#'+id_,'pdf_page':anchors[id_]['page'],'source':'figures/figures.json'})
    coverage={'schema':'axispl.actual-product-coverage.v1','candidate':CANDIDATE,'pdf':'report/Vitreos_AxisPL_Evidence_Atlas.pdf','pdf_sha256':hashlib.sha256((root/'report/Vitreos_AxisPL_Evidence_Atlas.pdf').read_bytes()).hexdigest(),'pdf_pages':len(document.pages),'entries':rows,'rendered_anchors':anchors,'supplement':{'html_anchor':'index.html#A08','report_anchor':'report/report.html#A08','pdf_page':anchors['A08']['page'],'source':'manuscript/evidence.md','catalog':'data/artifact-catalog.public.json'},'limits':'Real rendered destinations; coverage alone does not establish visual, scientific, security or publication acceptance.'}
    coverage['artifact_groups']=[{'id':g['id'],'html_anchor':'index.html#'+g['id'],'catalog_anchor':'evidence.html#'+g['id'],'pdf_page':anchors[g['id']]['page'],'source':'data/artifact-catalog.public.json'} for g in load(root,'data/artifact-catalog.public.json')['groups']]
    (root/'coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
    print(json.dumps({'pages':len(document.pages),'coverage_entries':len(rows),'pdf_sha256':coverage['pdf_sha256']}))

if __name__=='__main__':main()
