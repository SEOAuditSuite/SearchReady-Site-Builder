#!/usr/bin/env python3
"""Browser test of the actual variant script using synthetic DOM, not Shopify runtime."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os,json,sys,shutil
R=Path(__file__).resolve().parents[1]
HTML='''<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body><form><p data-current-price aria-live="polite">$10.00</p><label for="variant">Choose an option</label><select id="variant" name="id" data-variant-picker><option value="1" data-available="true" data-price="$10.00">Blue</option><option value="2" data-available="true" data-price="$14.00">Yellow</option><option value="3" data-available="false" data-price="$16.00" disabled>Pink — Sold out</option></select><button data-add type="submit">Add to bag</button></form></body></html>'''
checks=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path=shutil.which('chromium') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
  page=browser.new_page(viewport={'width':375,'height':800}); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(HTML);page.add_script_tag(path=str(R/'shopify/paper-spark/assets/variants.js'))
  checks.append(('initial price and enabled button',page.locator('[data-current-price]').inner_text()=='$10.00' and page.locator('[data-add]').is_enabled()))
  page.locator('select').select_option('2');checks.append(('available variant price',page.locator('[data-current-price]').inner_text()=='$14.00' and page.locator('[data-add]').is_enabled()))
  page.locator('select').evaluate("el=>{el.value='3';el.dispatchEvent(new Event('change'))}");checks.append(('unavailable variant disables submit',page.locator('[data-add]').is_disabled() and page.locator('[data-add]').inner_text()=='Sold out'))
  page.locator('select').select_option('1');checks.append(('return to available variant',page.locator('[data-add]').is_enabled() and page.locator('[data-current-price]').inner_text()=='$10.00'))
  checks.append(('no page errors',not errors)); browser.close()
except Exception as e:
 print(json.dumps({'scope':'synthetic DOM, actual JS','status':'BLOCKED','reason':str(e)[:500]},indent=2));sys.exit(2)
print(json.dumps({'scope':'synthetic DOM, actual JS; not Shopify runtime','checks':[{'name':n,'status':'PASS' if ok else 'FAIL'} for n,ok in checks],'pass':sum(ok for n,ok in checks),'fail':sum(not ok for n,ok in checks)},indent=2));sys.exit(0 if all(ok for n,ok in checks) else 1)
