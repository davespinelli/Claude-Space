# Precision check - validation sample of the recommended clean event

Fresh random draw (seed 20260924) from the FIRST-PASS clean-event definition (non-financial filers, original 8-K / 10-Q / 10-K, phrase "operating leverage", no "negative operating leverage" / "operating deleverage" in the same filing). Two of the 30 turned out to be negatives phrased as "reduced operating leverage", which is why the final definition also drops filings that match the supplementary negative phrases and SPAC-named filers. See the scoring table at the bottom of precision_sample.md for how the final definition does on these files.

| label | n | share |
|---|---:|---:|
| (a) management describing its own operating leverage as positive / improving | 27 | 90% |
| (b) negative operating leverage / deleveraging | 2 | 7% |
| (c) risk-factor, forward-looking-statement or other boilerplate | 1 | 3% |
| (d) bank / financial-company usage (efficiency-ratio sense) | 0 | 0% |
| (e) other (definitions, generic discussion, third-party, etc.) | 0 | 0% |
| total | 30 | |

Within (a): realized 13 (43% of sample), forward 9 (30% of sample), model-claim 5 (17% of sample).

Files skipped in the draw (unusable, replaced by the next draw): 0

Cross-tab by filer type and document type:

| filer | document | a | b | c | d | e |
|---|---|---:|---:|---:|---:|---:|
| non-financial | 10-K main | 10 | 0 | 0 | 0 | 0 |
| non-financial | 10-Q main | 4 | 1 | 0 | 0 | 0 |
| non-financial | 8-K earnings release (Item 2.02 EX-99) | 7 | 1 | 0 | 0 | 0 |
| non-financial | 8-K other | 6 | 0 | 1 | 0 | 0 |

---

### 1. Starry Group Holdings, Inc.  (CIK 0001884697) - 8-K 2022-08-09 - `stry-ex99_1.htm` -> **(a) / realized**
SIC 4813; doc_role=ex99; earnings 8-K=True; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1884697/000095017022015757/stry-ex99_1.htm)

*Why:* Earnings release: executed plan while improving the operating leverage in the business.

> ...rovider, today reported full results for the second quarter of 2022. The results showed that Starry has continued to successfully execute on its business plan, delivering a strong increase in customer relationships and driving an increase in penetration of homes serviceable, all while improving the **operating leverage** in the business. Additionally, Starry continued to expand the reach of its digital equity program, Starry Connect, growing the program to reach more than 77,400 units of public and affordable housing as of June 30, 2022, an increase of more than 14,300 in the quarter, all of which are automatically...

### 2. Inotiv, Inc.  (NOTV)  (CIK 0000720154) - 10-K 2021-12-21 - `notv-20210930x10k.htm` -> **(a) / realized**
SIC 8731; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/720154/000155837021016976/notv-20210930x10k.htm)

*Why:* 10-K MD&A: cost of services/revenue fell due primarily to improved operating leverage.

> ...or the year ended September 30, 2021 was $59,450 or 66.3% of revenue compared to $42,232 or 69.8% of revenue for the prior fiscal year. Cost of Services revenue as a percentage of Services revenue decreased to 66.7% in fiscal 2021 compared to 70.0% in the prior fiscal year due primarily to improved **operating leverage** and the greater utilization of recently expanded capacity. Cost of Products revenue as a percentage of Products revenue in fiscal 2021 decreased to 58.0% from 67.6% in the prior fiscal year. This decrease in fiscal 2021 is mainly due to expense reductions implemented in the last half of fiscal 2020...

### 3. SITO MOBILE, LTD.  (CIK 0001157817) - 8-K 2016-09-15 - `f8k091216ex99i_sitomobile.htm` -> **(a) / model-claim**
SIC 7389; doc_role=ex99; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1157817/000121390016016815/f8k091216ex99i_sitomobile.htm)

*Why:* Investor deck bullet: 'Significant operating leverage'.

> ...T DEVELOPMENT WIRELESS RETAIL INC. JULIANE HORTON EVP , PEOPLE & CULTURE KATE FARLEY EVP , STRATEGY & SALES MARKETING FINANCIAL AND OPERATIONAL HIGHLIGHTS 23 Exceptionally strong, capital efficient, top line growth Diversified and growing customer base which is increasing campaign spend Significant **operating leverage** Scalable, technology driven business model 1 2 4 5 Superior technology driving growth in campaign volumes and average size 3 Double Vision acquisition Seasonality Monthly Impressions Unique Campaign Count TREMENDOUS MOMENTUM IN CAMPAIGN VOLUME AND SIZE 24 79% YOY Growth • Benefiting from larger cli...

### 4. SAIA INC  (SAIA)  (CIK 0001177702) - 10-K 2026-02-24 - `saia-20251231.htm` -> **(a) / forward**
SIC 4213; doc_role=main; earnings 8-K=False; occurrences in file=3; [link](https://www.sec.gov/Archives/edgar/data/1177702/000119312526067030/saia-20251231.htm)

*Why:* 10-K business strategy: gain operating leverage by growing density (same text Saia has used since at least 2011; see main sample 2).

> ...ity of our network. In recent years, our expanded geographic footprint and strengthened service offerings have enabled us to deliver differentiated solutions to customers, contributing to increases in revenue per shipment, excluding fuel surcharges. Increase density in existing geographies. We gain **operating leverage** by growing volume and density within our existing geography. Depending on general economic conditions, pricing and the specific geography, we estimate that the potential incremental profitability on growth in current markets can be significant. We continuously evaluate opportunities to expand our t...

> ...nticipates the impact will be partially offset by productivity and efficiency gains. The strategic objective of the Company is to build market share through excellent customer service, continued operating efficiencies and through its geographic and terminal expansion which should result in numerous **operating leverage** cost benefits. However, should the economy soften, the Company plans to match resources and capacity to shifting volume levels to lessen unfavorable **operating leverage**. The success of cost improvement initiatives is impacted by a number of factors. These factors include the cost and availability of...

### 5. Aterian, Inc.  (ATER)  (CIK 0001757715) - 8-K 2021-12-27 - `d280987dex991.htm` -> **(c) / boilerplate**
SIC 3634; doc_role=ex99; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1757715/000119312521367017/d280987dex991.htm)

*Why:* Forward-looking-statements legend: 'our ability to create operating leverage and efficiency when integrating companies'.

> ...isks include, but are not limited to; those related to the global shipping disruptions, our ability to continue as a going concern, our ability to continue to secure preferred shipping rates with our logistics partners, our ability to meet financial covenants with our lenders, our ability to create **operating leverage** and efficiency when integrating companies that we acquire, including through the use of our team’s expertise, the economies of scale of our supply chain and automation driven by our platform; those related to our ability to grow internationally and through the launch of products under our brands an...

### 6. TransUnion  (TRU)  (CIK 0001552033) - 10-K 2026-02-27 - `tru-20251231.htm` -> **(a) / model-claim**
SIC 7320; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1552033/000155203326000012/tru-20251231.htm)

*Why:* 10-K business overview: attractive model with 'significant operating leverage'.

> ...ternational markets. Millions of consumers across the globe use our data and tools to manage their personal finances and take precautions against identity theft. We believe we have an attractive business model that has recurring and diversified revenue streams, low capital requirements, significant **operating leverage** and strong and stable cash flows. The proprietary and embedded nature of our solutions and the integral role that we play in our customers’ decision-making processes have historically translated into high customer retention and revenue visibility. We deliver organic growth by growing our transactio...

### 7. BRUNSWICK CORP  (BC, BC-PC)  (CIK 0000014930) - 8-K 2026-07-30 - `q22026exhibit99_1.htm` -> **(a) / realized**
SIC 3510; doc_role=ex99; earnings 8-K=True; occurrences in file=2; [link](https://www.sec.gov/Archives/edgar/data/14930/000001493026000087/q22026exhibit99_1.htm)

*Why:* Earnings release: segment profitability underscores attractive operating leverage; strong operating leverage behind higher margin outlook.

> ...ne Parts and Accessories delivered another strong quarter, supported by healthy boating participation and the resultant demand for products along with past pricing actions. The Products and Distribution businesses both contributed to improved profitability, underscoring the stability and attractive **operating leverage** of this recurring-revenue business. Navico Group continued its strong performance trajectory, with sales growth across its business lines supported by new products, OEM wins, sustained aftermarket demand, and ongoing operational improvement actions. The business also advanced strategic opportunitie...

> ...act heavily weighted to the first half. Our updated earnings outlook also reflects approximately $25 to $30 million of net IEEPA refunds expected to be recognized in 2026, inclusive of the resulting impact on enterprise-wide compensation. Together with continued business improvement actions, strong **operating leverage**, and mix benefits, we expect materially higher adjusted operating margin this year, while maintaining our commitment to keeping pipelines healthy and preserving balance-sheet strength," said Foulkes. “Using our best estimates related to these items and all other business impacts, the following is o...

### 8. CARRIAGE SERVICES INC  (CSV)  (CIK 0001016281) - 8-K 2011-10-13 - `h85093exv99w2.htm` -> **(a) / model-claim**
SIC 7200; doc_role=ex99; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1016281/000095012311089722/h85093exv99w2.htm)

*Why:* Investor deck: volume trends critical for maintaining operating leverage benefits of a high-fixed-cost network.

> ...entralized high-performance culture framework and linked incentive compensation program attracts top-quality industry talent at both regional and corporate level. Long term (five year) funeral and interment volume trends are most favorable in deathcare industry, which is critical for maintenance of **operating leverage** benefits in high fixed cost distribution network of local operating businesses. Long term, low fixed rate capital structure components enable strong and growing Free Cash Flow from existing operations to finance about 75% of acquisition growth pursuant to our published five year plan, while improvi...

### 9. Vacasa, Inc.  (VCSA)  (CIK 0001874944) - 10-K 2023-03-15 - `vcsa-20221231.htm` -> **(a) / forward**
SIC 7340; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1874944/000187494423000018/vcsa-20221231.htm)

*Why:* 10-K MD&A: expects EBITDA margin to improve over the medium/long term as it achieves operating leverage from scale.

> ...djusted EBITDA as a percentage of revenue, as fixed costs are allocated across a larger number of guest reservations. We expect Adjusted EBITDA and Adjusted EBITDA as a percentage of revenue to fluctuate in the near term due to this seasonality and improve over the medium to long term as we achieve **operating leverage** from scale and density. Adjusted EBITDA was $(27.5) million for the year ended December 31, 2022, compared to $(28.5) million for the year ended December 31, 2021. The favorable change in Adjusted EBITDA is a reflection of the changes in our revenue, operating costs, and expenses, as discussed abov...

### 10. TENNANT CO  (TNC)  (CIK 0000097134) - 10-K 2014-02-28 - `form_10-k.htm` -> **(a) / realized**
SIC 3580; doc_role=main; earnings 8-K=False; occurrences in file=3; [link](https://www.sec.gov/Archives/edgar/data/97134/000009713414000008/form_10-k.htm)

*Why:* 10-K MD&A: S&A/sales fell on cost control and improved operating leverage.

> ... 44.0% in 2012 due to changes in selling channel mix and mix of products sold. Selling and Administrative Expense (“S&A Expense”) decreased 0.5% , or 70 basis points as a percentage of Net Sales, from $234.1 million in 2012 to $233.0 million in 2013 due to continued tight cost controls and improved **operating leverage**. Operating Profit decreased 0.5% and Operating Profit margin declined 20 basis points to 8.3% in 2013 from 8.5% in 2012 due to two restructuring charges taken during 2013 totaling $3.0 million and increased investment in R&D activities. Net Earnings for 2013 were favorably impacted by a tax benefit...

> ...ly flat with growth in the Americas and emerging markets being offset by declines in the mature international markets. S&A Expense decreased 3.1%, or 30 basis points as a percentage of Net Sales, from $241.6 million in 2011 to $234.1 million in 2012 due to continued tight cost controls and improved **operating leverage**. Operating Profit increased 26.3% and Operating Profit margin improved 190 basis points to 8.5% in 2012 from 6.6% in 2011 due to higher Gross Profits and improved **operating leverage**. Net Earnings for 2012 were also favorably impacted by a $2.0 million tax benefit from an international entity restru...

### 11. Alkermes plc.  (ALKS)  (CIK 0001520262) - 8-K 2021-01-11 - `alks-ex991_15.htm` -> **(a) / forward**
SIC 2834; doc_role=ex99; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1520262/000156459021000748/alks-ex991_15.htm)

*Why:* Investor deck: optimize cost structure and drive operating leverage.

> ...stration pathway Demonstrate anti-tumor activity Explore strategic collaboration ALKS 1140 (CoREST-selective HDAC inhibitor) Initiate phase 1/FIH study Investor Day Provide update on pipeline platforms and programs Operationalize commitment to profitability targets Optimize cost structure and drive **operating leverage** Explore strategic opportunities to maximize value and enhance profitability 1 2 3 *Prescription Drug User Fee Act Value Enhancement Plan and Board Refreshment Profitability Targets and Cost Structure Optimization Evaluation of Strategic Opportunities Board Refreshment Commitment to achieving: Ongoi...

### 12. Builders FirstSource, Inc.  (BLDR)  (CIK 0001316835) - 10-Q 2024-11-05 - `bldr-20240930.htm` -> **(b) / negative**
SIC 5211; doc_role=main; earnings 8-K=False; occurrences in file=2; [link](https://www.sec.gov/Archives/edgar/data/1316835/000095017024121436/bldr-20240930.htm)

*Why:* 10-Q MD&A: SG&A/sales rose, primarily attributable to reduced operating leverage.

> ...-offs, which were partially offset by lower variable compensation on decreased sales. As a percentage of net sales, selling, general and administrative expenses increased to 22.6%, up from 20.7%, for the three months ended September 30, 2024 and 2023, respectively, primarily attributable to reduced **operating leverage**. Interest Expense, Net. Interest expense was $54.3 million in the third quarter of 2024, an increase of $4.1 million from the third quarter of 2023. The increase was due to higher average debt balances. Income Tax Expense. We recorded income tax expense of $89.0 million and $140.0 million in the th...

> ...ng expenses from locations acquired within the last twelve months and asset write-offs. As a percentage of net sales, selling, general and administrative expenses increased to 22.7%, up from 22.1% for the nine months ended September 30, 2024 and 2023, respectively, primarily attributable to reduced **operating leverage**. Interest Expense, Net. Interest expense was $154.6 million in the nine months ended September 30, 2024, an increase of $9.3 million from the nine months ended September 30, 2023. Interest expense increased primarily due to higher debt balances partially offset by interest income received in 2024. ...

### 13. BOISE CASCADE Co  (BCC)  (CIK 0001328581) - 8-K 2014-03-10 - `irpresentationmarch2014.htm` -> **(a) / forward**
SIC 5030; doc_role=ex99; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1328581/000132858114000012/irpresentationmarch2014.htm)

*Why:* IR deck: recent capacity additions provide significant operating leverage opportunity.

> ...g geographic markets/branches • Leverage advantages of national scale • Opportunistically expand into adjacent markets Source: U.S. Census Bureau and Blue Chip Economic Indicators. BMD Sales per U.S. Start and Gross Margin Significant Available Capacity Recent capacity additions provide significant **operating leverage** opportunity in BMD 6 Wood Products Manufacturing Value Chain Veneer Purchased Logs Plywood I-joist Conversion Costs Conversion Costs Conversion Costs Purchased Veneer / Lumber / OSB Purchased Plywood Maximize total return on raw materials purchased LVL 7 Housing Starts (mm): 1.801 1.355 0.906 0.554...

### 14. OBALON THERAPEUTICS INC  (RSLS)  (CIK 0001427570) - 10-K 2017-02-23 - `obln-123116x10k.htm` -> **(a) / forward**
SIC 3841; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1427570/000162828017001603/obln-123116x10k.htm)

*Why:* 10-K strategy: optimize manufacturing to drive operating leverage.

> ...t pipeline include a navigation system that would reduce the need for imaging at every placement, a balloon with a treatment period of longer than six months and a self-deflating and self-passing balloon that could eliminate the need for endoscopic balloon removal. ▪ Optimize manufacturing to drive **operating leverage**. We have built a highly leverageable manufacturing facility at our headquarters in Carlsbad, California, where we design, develop and manufacture our products in-house using some components and sub-assemblies provided by third-party suppliers. We believe that controlling the manufacturing and assem...

### 15. Q2 Holdings, Inc.  (QTWO)  (CIK 0001410384) - 10-K 2019-02-19 - `a181231qtwo10k.htm` -> **(a) / forward**
SIC 7372; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1410384/000141038419000015/a181231qtwo10k.htm)

*Why:* 10-K MD&A: anticipates economies of scale and increased operating leverage will improve margins long term.

> ... of our realizing any resultant benefit which may make it difficult to determine if we are effectively allocating our resources. If we are successful in growing our revenues by increasing the number and scope of our customer relationships, we anticipate that greater economies of scale and increased **operating leverage** will improve our margins over the long term. We also anticipate that increases in the number of Registered Users for existing digital banking platform customers will improve our margins. However, we do not have any control or influence over whether End Users of our digital banking platform elect to...

### 16. Rocket Lab Corp  (RKLB)  (CIK 0001819994) - 10-K 2026-02-26 - `rklb-20251231.htm` -> **(a) / forward**
SIC 3760; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000013/rklb-20251231.htm)

*Why:* 10-K MD&A: will invest to improve operating leverage and ramp production.

> ... To sell additional products and services to new and existing customers, we will need to continue to invest significant resources in our products and services. 44 Table of Contents Ability to improve profit margins and scale our business We intend to continue to invest in initiatives to improve our **operating leverage** and significantly ramp production. We believe continued reduction in costs and an increase in production volumes will enable the cost of launch vehicles to decline and improve our gross margins. Our ability to achieve our production-efficiency objectives could be negatively impacted by a variety of...

### 17. Ranger Energy Services, Inc.  (RNGR)  (CIK 0001699039) - 8-K 2026-07-27 - `rngr-063026ex991earningsre.htm` -> **(a) / realized**
SIC 1389; doc_role=ex99; earnings 8-K=True; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1699039/000162828026049852/rngr-063026ex991earningsre.htm)

*Why:* Earnings release: improved operating income reflects higher activity and strong operating leverage.

> ...llion in the prior year period. Adjusted EBITDA (1) was $3.6 million, an increase from $0.2 million in the first quarter of 2026 and an increase from $1.6 million in the second quarter of 2025. The improved operating income and Adjusted EBITDA reflect higher activity across service lines and strong **operating leverage** with improved efficiency. BALANCE SHEET, CASH FLOW AND LIQUIDITY As of June 30, 2026, the Company had total liquidity of $61.3 million, consisting of $57.1 million of available capacity under its revolving credit facility and $4.2 million of cash on hand. This compares to total liquidity of $67.7 m...

### 18. IXIA  (CIK 0001120295) - 10-K 2017-03-01 - `a2016q4form10-k.htm` -> **(a) / realized**
SIC 3825; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1120295/000112029517000006/a2016q4form10-k.htm)

*Why:* 10-K MD&A: cost of revenue share fell partly on incremental operating leverage from higher revenues.

> ...total revenues, our total cost of revenues decreased to 22.0% in the year ended December 31, 2015 from 24.8% in year ended December 31, 2014. This percentage decrease was primarily due to the realization of higher gross margins on certain of our products in 2015, and to a lesser extent, incremental **operating leverage** associated with higher revenues and relatively fixed indirect costs. Cost of revenues does not include the amortization of purchased technology related to our acquisitions of certain businesses, product lines, and technologies of $25.7 million and $28.9 million for the years ended December 31, 2015...

### 19. Confluent, Inc.  (CFLT)  (CIK 0001699838) - 10-Q 2025-04-30 - `cflt-20250331.htm` -> **(a) / model-claim**
SIC 7372; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1699838/000095017025061127/cflt-20250331.htm)

*Why:* 10-Q MD&A: large customer relationships lead to scale and operating leverage in our business model.

> ...months, calculated by annualizing actual consumption of Confluent Cloud and WarpStream in the last three months of the applicable period, assuming no increases or reductions in usage rate. Services arrangements are excluded from the calculation of ARR. Large customer relationships lead to scale and **operating leverage** in our business model. Compared with smaller customers, large customers present a greater opportunity for us because they have larger budgets, greater potential for migrating more applications over time, and a wider range of potential use cases for data in motion. As a measure of our ability to sca...

### 20. SKULLCANDY, INC.  (CIK 0001423542) - 10-K 2016-03-04 - `skul123115-10xk.htm` -> **(a) / realized**
SIC 3651; doc_role=main; earnings 8-K=False; occurrences in file=2; [link](https://www.sec.gov/Archives/edgar/data/1423542/000142354216000112/skul123115-10xk.htm)

*Why:* 10-K MD&A: SG&A/sales fell due to better operating leverage.

> ...thousands): Year Ended December 31, 2015 2014 $ Change % Change Selling, general and administrative expenses $ 100,903 $ 98,847 $ 2,056 2.1 % Selling, general and administrative expenses as a percent of net sales 37.9 % 39.9 % While SG&A expenses as a percentage of net sales decreased due to better **operating leverage** of our expenses, the overall increase in SG&A expenses is primarily due to increased bad debt expense of $1.6 million related to a China distributor, increased demand creation and product creation expenses, partially offset by decreases in personnel related expenses. We expect to make critical inve...

> ...in thousands): Year Ended December 31, 2014 2013 $ Change % Change Selling, general and administrative expenses $ 98,847 $ 98,129 $ 718 0.7 % Selling, general and administrative expenses as a percent of net sales 39.9 % 46.7 % While SG&A expenses as a percentage of net sales decreased due to better **operating leverage** of our expenses, the overall increase in SG&A expenses is primarily due to an increase in marketing, demand creation and product creation expenses, personnel related expenses and increased third party commission expense as a result of higher sales, partially offset by decreases in bad debt expense....

### 21. VWR Corp  (CIK 0001412232) - 10-Q 2015-11-05 - `a2015q3form10-qc.htm` -> **(a) / realized**
SIC 5040; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1412232/000141223215000041/a2015q3form10-qc.htm)

*Why:* 10-Q MD&A: comparable operating income rose as a result of better operating leverage.

> ...cialized offerings by our largest customers. • Comparable operating income was impacted by a number of distinct SG&A items, detailed below under “SG&A Expenses.” When excluding the impact of these items, comparable operating income and comparable Adjusted EBITDA each increased as a result of better **operating leverage**. These increases were partially offset by two transitory factors related to EMEA-APAC, discussed further below under “Gross Profit.” In addition, a less favorable product sales mix and changes to a supply agreement negatively impacted the year-to-date comparison. • Adjusted Net Income and Adjusted ...

### 22. Meritage Homes CORP  (MTH)  (CIK 0000833079) - 8-K 2013-07-24 - `mth-2013_q2xexhibit991.htm` -> **(a) / realized**
SIC 1531; doc_role=ex99; earnings 8-K=True; occurrences in file=5; [link](https://www.sec.gov/Archives/edgar/data/833079/000083307913000108/mth-2013_q2xexhibit991.htm)

*Why:* Earnings release: additional operating leverage drove 252% earnings growth; commissions and G&A improved on operating leverage.

> ...ive quarter of positive year-over-year growth in orders and our seventh consecutive quarter of growth in closing revenue year over year. "More importantly, our earnings continued to grow at a much higher rate than our revenue. Our gross margin on home closings increased to 21.5%, and our additional **operating leverage** drove year-over-year net earnings growth of 252% on a 55% increase in home closing revenue. “ Despite the recent rise in interest rates and home prices, affordability remains excellent and demand for new homes continues to be strong in our markets, as evidenced by our pace of orders increasing over...

> ...for the second quarter of 2013 from 9.0 in the second quarter of 2012 and 9.5 in the first quarter of 2013. • Meritage ended the quarter with 165 active communities, up from 151 at June 30, 2012. • Order cancellation rate fell to 11% in the second quarter of 2013, compared to 13% in the prior year. **OPERATING LEVERAGE** • Net earnings for the second quarter increased 252% year over year to $28.1 million or $0.74 per diluted share in 2013, compared to $8.0 million or $0.24 per diluted share in 2012, primarily due to higher home closing revenue and gross margins, coupled with overhead expense leverage. • Home closin...

> ...2012, and a sequential improvement of 200 bps compared to 19.5% in the first quarter of 2013. The significant margin growth reflects both home price appreciation and the effects of improved management of direct costs. • Commissions and other sales costs in the second quarter improved 100 bps due to **operating leverage**, decreasing as a percentage of home closing revenue to 7.2% in 2013 from 8.2% in 2012. • General and administrative expenses also improved 90 bps due to **operating leverage**, declining to 5.0% of second quarter revenue in 2013, from 5.9% in 2012. The majority of the $5.9 million increase over last ye...

### 23. Evolent Health, Inc.  (EVH)  (CIK 0001628908) - 8-K 2023-01-11 - `exhibit991.htm` -> **(a) / forward**
SIC 8741; doc_role=ex99; earnings 8-K=True; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1628908/000162890823000005/exhibit991.htm)

*Why:* Investor deck: 'Mix Shift, Scale, Operating Leverage Drive Margin Expansion'.

> ...while also reducing the cost of care. The result will help us provide even better care for our members, while making our plans more affordable.” George Renaudin President Medicare, Humana Florida Case Study: Payers On Performance Suite National Payer 2 14 Investment Considerations Mix Shift, Scale, **Operating Leverage** Drive Margin Expansion • Reiterating 2022 outlook: $98-$103M of Adjusted EBITDA, implying a 7.4% Adjusted EBITDA margin at the midpoint1 • Adjusted EBITDA and cash flow positive with multiple opportunities for growth and expansion • Mix shift to full risk performance suite in oncology and cardiolog...

### 24. STR Holdings, Inc.  (CIK 0001473597) - 10-Q 2010-05-12 - `a10-6231_110q.htm` -> **(a) / realized**
SIC 3081; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1473597/000110465910027982/a10-6231_110q.htm)

*Why:* 10-Q MD&A: gross margin up on increased operating leverage of fixed costs.

> ...d in 2009 primarily due to the sales increase in our Solar segment. As a percentage of sales, gross profit increased 310 basis points from 34.6% for the three months ended March 31, 2009 to 37.7% for the same period in 2010. Gross profit increased as a percentage of sales primarily due to increased **operating leverage** of fixed costs associated with our Solar sales volume increase, partially offset by lower pricing and increased raw material costs in our Solar segment and higher labor cost incurred by our Quality Assurance segment. Also, we generated a higher mix of net sales in our higher margin Solar business, ...

### 25. BIG 5 SPORTING GOODS Corp  (BGFV)  (CIK 0001156388) - 8-K 2021-03-02 - `d144124dex991.htm` -> **(a) / realized**
SIC 5940; doc_role=ex99; earnings 8-K=True; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1156388/000119312521065504/d144124dex991.htm)

*Why:* Earnings release CEO quote: cost reductions continue to provide significant operating leverage.

> ...r customers with a convenient shopping experience to find products to stay active and healthy. Our team did a tremendous job of recognizing and capitalizing on key product trends. Additionally, in 2020 we successfully implemented cost reduction initiatives that are continuing to provide significant **operating leverage**. Looking back on the year, I want to once again thank our entire team for their dedication and execution during a challenging period.” Mr. Miller continued, “The momentum of 2020 has continued into the start of 2021, with our same store sales up approximately 20% for the quarter to date. Although t...

### 26. CAMPBELL SOUP CO  (CPB)  (CIK 0000016732) - 8-K 2021-06-09 - `exhibit991-q32021.htm` -> **(b) / negative**
SIC 2000; doc_role=ex99; earnings 8-K=True; occurrences in file=3; [link](https://www.sec.gov/Archives/edgar/data/16732/000001673221000071/exhibit991-q32021.htm)

*Why:* Earnings release: gross margin down on inflation, mix and reduced operating leverage.

> ... of the COVID-19 pandemic in the prior-year quarter. Gross margin decreased to 31.7% from 34.5% last year. Excluding items impacting comparability, adjusted gross margin decreased 290 basis points to 31.8% as higher cost inflation and other supply chain costs, as well as unfavorable mix and reduced **operating leverage** were partially offset by a net benefit from the change in mark-to-market adjustments on outstanding commodity hedges, supply chain productivity improvements and cost savings initiatives. Marketing and selling expenses decreased 15% to $202 million driven by lower advertising and consumer promotion ...

> ... broth. Segment operating earnings decreased 35%. The decrease was primarily due to sales volume declines and lower gross margin performance partially offset by lower marketing and selling expenses. Gross margin performance was impacted by higher cost inflation and other supply chain costs, reduced **operating leverage** and unfavorable product mix, partially offset by the benefits of supply chain productivity improvements. Snacks Net sales in the quarter, both reported and organic, decreased 8% driven by volume declines within the salty snacks portfolio, including Pop Secret popcorn, Cape Cod potato chips and Snyd...

> ...rnings decreased 29% for the quarter driven by lower gross margin performance and sales volume declines, partially offset by lower marketing and selling expenses and lower administrative expenses. Gross margin performance was impacted by higher cost inflation and other 6 supply chain costs, reduced **operating leverage** and unfavorable product mix, partially offset by the benefits of supply chain productivity improvements. Corporate Corporate expenses were $14 million in the third quarter of fiscal 2021 compared to $156 million in the prior year. Corporate expenses in the third quarter of fiscal 2021 included cost...

### 27. INPHI Corp  (CIK 0001160958) - 8-K 2020-05-07 - `ex_185239.htm` -> **(a) / realized**
SIC 3674; doc_role=ex99; earnings 8-K=True; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1160958/000143774920009823/ex_185239.htm)

*Why:* Earnings release: non-GAAP operating income up on higher gross profit and higher operating leverage.

> ...t mix, mainly from the sale of eSilicon products that have a lower margin. Non-GAAP operating income in the first quarter of 2020 was $34.2 million, compared with non-GAAP operating income of $15.6 million in the first quarter of 2019. The increase is primarily due to higher gross profit and higher **operating leverage**. Non-GAAP net income in the first quarter of 2020 was $31.5 million, or $0.62 per diluted common share. This compares with non-GAAP net income of $15.4 million, or $0.33 per diluted common share in the first quarter of 2019. The Company spent approximately $215 million to acquire eSilicon on Januar...

### 28. DELTA AIR LINES INC /DE/  (DAL)  (CIK 0000027904) - 8-K 2015-09-09 - `dal_8k-ex9901.htm` -> **(a) / forward**
SIC 4512; doc_role=ex99; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/27904/000101968715003407/dal_8k-ex9901.htm)

*Why:* Investor update: improved operating leverage to be achieved as aircraft upgauging continues.

> ...0.2% - 1.1% 2012 2013 2014 YTD 2Q15 Non - Fuel Unit Cost Growth Excludes special items Solid financial plan in place to deliver second consecutive year of sub - 2% unit cost growth • Benefits from upgauging, maintenance savings and commercial productivity initiatives continue – Upgauging : Improved **operating leverage** to be achieved as modifications continue and increase the gauge on roughly 260 aircraft – Refleeting : Retirement of 747s, older 757s and domestic 767s drive almost $200 million of maintenance savings in 2015 – Maintenance: Ongoing utilization of part - out materials – Supply Chain: Leveraging scal...

### 29. TECH DATA CORP  (CIK 0000790703) - 10-Q 2010-09-01 - `d10q.htm` -> **(a) / realized**
SIC 5045; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/790703/000119312510202839/d10q.htm)

*Why:* 10-Q MD&A: SG&A/sales fell on the operating leverage achieved as sales grew faster than opex.

> ...percentage of net sales decreased to 4.01% compared to 4.21% in the comparable semester of the prior fiscal year .The decrease in SG&A as a percentage of net sales in the second quarter and first semester of fiscal 2011 compared to the same periods of the prior year is primarily attributable to the **operating leverage** achieved this year as our net sales have increased at a more rapid rate than our operating expenses. In absolute dollars, SG&A increased by $6.6 million in the second quarter of fiscal 2011 compared to the second quarter of fiscal 2010 and increased by $16.5 million in the first semester of fiscal ...

### 30. Wayside Technology Group, Inc.  (CLMB)  (CIK 0000945983) - 8-K 2018-09-26 - `a18-35000_1ex99d1.htm` -> **(a) / model-claim**
SIC 5045; doc_role=ex99; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/945983/000110465918058786/a18-35000_1ex99d1.htm)

*Why:* Investor deck business model: 'high operating leverage and low capital investment requirements'.

> ...8 • • 12 Adjusted Gross Billings Growth 2016-Rates 2017 CAGR 1H 2018 Growth Rate Hardware & Software product -1.5% Maintenance and service 8.6% Software - security 25.2% Total 8.4% 10.3% 8.7% 18.8% 12.0% BUSINESS MODEL Our business is characterized by low gross profit as a % of gross billings, high **operating leverage** and low capital investment requirements, resulting in mid teen return on invested capital. Return on invested capital is calculated as net income/(shareholders equity + debt - cash) 13 Full Year 2017 Historical Accounting ASC 606 Adjusted gross billings/net sales $ 449.4 $ 160.6 Gross margin $ 27.1...
