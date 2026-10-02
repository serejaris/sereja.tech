from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
report=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for key in ['home','post','blog','about','links','tags','topic','error','rich']:
  page=b.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8766/after-'+key+'.html',wait_until='networkidle')
  page.screenshot(path=str(R/'screens'/f'after-{key}.png'))
  row={'page':key,'h1':page.locator('h1').count(),'overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth'),'tables':page.locator('table').count(),'errors':errors}
  report.append(row);print(row,flush=True)
  if key=='post':
   page.locator('h2').first.scroll_into_view_if_needed();page.screenshot(path=str(R/'screens'/'after-post-body.png'))
   page.locator('.prompt-card').scroll_into_view_if_needed();page.locator('.prompt-card summary').click();page.screenshot(path=str(R/'screens'/'after-post-prompt.png'))
  if key=='blog':
   page.locator('#search').fill('агент');page.screenshot(path=str(R/'screens'/'after-search.png'))
   row['search_results']=page.locator('#result-count').inner_text()
   page.locator('#search').fill('zzzxxyy');page.screenshot(path=str(R/'screens'/'after-empty.png'));row['empty_state']=page.locator('#empty').is_visible()
   page.locator('#reset').click();page.locator('[data-topic="agents"]').click();row['topic_results']=page.locator('#result-count').inner_text();page.screenshot(path=str(R/'screens'/'after-cluster.png'))
  if key=='rich':
   page.locator('#usilie').scroll_into_view_if_needed();page.screenshot(path=str(R/'screens'/'after-rich-chart.png'))
   page.locator('#next-chart').click();row['chart_next']=page.locator('#chart-count').inner_text()
  page.close()
 b.close()
(R/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
