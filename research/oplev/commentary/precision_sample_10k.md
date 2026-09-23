# Precision check - 10-K-only sample (risk-factor check)

Random draw (seed 20260925) of 10-K files matching "operating leverage" (all filers), to check how often the phrase sits in Item 1A risk factors or other boilerplate. Same labelling rules; the note says where in the 10-K the phrase sits.

| label | n | share |
|---|---:|---:|
| (a) management describing its own operating leverage as positive / improving | 5 | 25% |
| (b) negative operating leverage / deleveraging | 0 | 0% |
| (c) risk-factor, forward-looking-statement or other boilerplate | 6 | 30% |
| (d) bank / financial-company usage (efficiency-ratio sense) | 6 | 30% |
| (e) other (definitions, generic discussion, third-party, etc.) | 3 | 15% |
| total | 20 | |

Within (a): realized 3 (15% of sample), forward 2 (10% of sample).

Files skipped in the draw (unusable, replaced by the next draw): 0

Cross-tab by filer type and document type:

| filer | document | a | b | c | d | e |
|---|---|---:|---:|---:|---:|---:|
| financial (SIC 6000-6999) | 10-K main | 0 | 0 | 3 | 6 | 0 |
| non-financial | 10-K main | 5 | 0 | 3 | 0 | 2 |
| non-financial | 10-K other_exhibit | 0 | 0 | 0 | 0 | 1 |

---

### 1. Athene Holding Ltd  (ATHS, ATH-PA, ATH-PB, ATH-PC, ATH-PD, ATH-PE)  (CIK 0001527469) - 10-K 2022-02-25 - `ahl-20211231.htm` -> **(d) / financial**
SIC 6311; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1527469/000152746922000018/ahl-20211231.htm)

*Why:* Insurer (SIC 6311), investment philosophy: operating leverage inherent in the business amplifies investment outperformance.

> ... incremental yield by taking measured liquidity risk and complexity risk and capitalizing on our long-dated and persistent liability profile to prudently achieve higher net investment earned rates, rather than assuming solely credit risk. A cornerstone of our investment philosophy is that given the **operating leverage** inherent in our business, modest investment outperformance can translate to outsized return performance. Because we have remained disciplined in underwriting attractively priced liabilities, we have the ability to invest in a broad range of high-quality assets to generate attractive earnings. Our d...

### 2. ARCBEST CORP /DE/  (ARCB)  (CIK 0000894405) - 10-K 2018-02-28 - `arcb-20171231x10k.htm` -> **(e) / structural**
SIC 4213; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/894405/000155837018001312/arcb-20171231x10k.htm)

*Why:* MD&A list of results drivers: tonnage 'influences operating leverage as tonnage levels vary'; recurring, no direction claimed.

> ...tand the operating results of our Asset-Based segment include: · overall customer demand for Asset-Based transportation services, including the impact of economic factors; · volume of transportation services provided, primarily measured by average daily shipment weight (“tonnage”), which influences **operating leverage** as tonnage levels vary; · prices obtained for services, primarily measured by yield (“revenue per hundredweight”), including fuel surcharges; and · ability to manage cost structure, primarily in the area of salaries, wages, and benefits (“labor”), with the total cost structure measured by the perce...

### 3. Brownie's Marine Group, Inc  (BWMG)  (CIK 0001166708) - 10-K 2020-06-29 - `ex10-19.htm` -> **(e) / third-party**
SIC 3949; doc_role=other_exhibit; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1166708/000149315220011971/ex10-19.htm)

*Why:* Exhibit 10.19 (investor-relations consulting agreement) listing topics to articulate, incl. operating leverage.

> ...to be articulated to the investing public includes: ● A better understanding of the core growth opportunities and key drivers for the end-market being addressed – this will be a recasting and development of the investment thesis; ● The extent of the Company’s growth plans, capital requirements, and **operating leverage**; ● Establishing and articulating the key operating, growth, and valuation metrics that investors/shareholders should focus on to judge future performance. Answering the question, “why should an investor invest in BWMG?” Shareholder Communications On a regular basis HIRH will contact known key share...

### 4. ThredUp Inc.  (TDUP)  (CIK 0001484778) - 10-K 2025-03-03 - `tdup-20241231.htm` -> **(c) / boilerplate**
SIC 5961; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1484778/000148477825000023/tdup-20241231.htm)

*Why:* Non-GAAP definition: Adjusted EBITDA used to assess the operating leverage in our business.

> ... Adjusted EBITDA (loss) from continuing operations divided by Total revenue. We use Non-GAAP Adjusted EBITDA (loss) from continuing operations and Non-GAAP Adjusted EBITDA (loss) from continuing operations margin, which are non-GAAP measures, to evaluate and assess our operating performance and the **operating leverage** in our business, and for internal planning and forecasting purposes. We believe that Non-GAAP Adjusted EBITDA (loss) from continuing operations and Non-GAAP Adjusted EBITDA (loss) from continuing operations margin, when taken collectively with our GAAP results, may be helpful to investors because t...

### 5. CBOE Holdings, Inc.  (CBOE)  (CIK 0001374310) - 10-K 2014-02-21 - `cboe-1231201310k.htm` -> **(d) / financial**
SIC 6200; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1374310/000137431014000008/cboe-1231201310k.htm)

*Why:* Exchange operator (SIC 6200): managing expense growth to drive greater operating leverage.

> ... lobby of our building; and • Other sources of revenue. 34 Table of Contents Components of Operating Expenses Most of our expenses do not vary directly with changes in our trading volume except royalty fees and trading volume incentives. We remain focused on managing expense growth to drive greater **operating leverage** and continue to explore opportunities to expand our operating margins. Employee Costs Employee costs are our most significant expense and include employee salaries, stock-based compensation, incentive compensation, severance, benefits and employer taxes. Salaries and benefits represent our largest ...

### 6. RF Acquisition Corp II  (RFAI, RFAIR, RFAIU)  (CIK 0002012807) - 10-K 2026-02-11 - `rfacq2_10k.htm` -> **(c) / boilerplate**
SIC 6770; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/2012807/000182912626001254/rfacq2_10k.htm)

*Why:* SPAC (SIC 6770) target-selection criteria boilerplate.

> ...ial . We will seek to acquire one or more businesses that have the potential for significant revenue and earnings growth through a combination of both existing and new product development, increased production capacity, expense reduction and synergistic follow-on acquisitions resulting in increased **operating leverage**. ● Potential for Strong Free Cash Flow Generation . We will seek to acquire one or more businesses that have the potential to generate strong, stable, and increasing free cash flow, particularly businesses with predictable revenue streams and definable low working capital and capital expenditure re...

### 7. FIRST DATA CORP  (CIK 0000883980) - 10-K 2018-02-21 - `a12311710-k.htm` -> **(a) / forward**
SIC 7389; doc_role=main; earnings 8-K=False; occurrences in file=2; [link](https://www.sec.gov/Archives/edgar/data/883980/000088398018000006/a12311710-k.htm)

*Why:* MD&A key initiatives: 'Maintain positive operating leverage'; restructuring to maintain it.

> ...e financial institutions with solutions to help them grow their revenues, enhance customer satisfaction, and deliver their products more timely and efficiently. We continue to execute on key initiatives: ◦ Innovate for tomorrow's client needs ◦ Accelerate top line revenue growth ◦ Maintain positive **operating leverage** ◦ Generate significant free cash flow 34 Components of Revenue We generate revenue by providing commerce-enabling solutions. Set forth below is a description of our revenues by segment and factors impacting total revenues. Global Business Solutions Global Business Solutions (GBS) revenues are prima...

> ...o our 270 basis points EBITDA margin expansion over the past three years. The Company has ongoing expense management initiatives, which are expected to result in approximately $20 million in additional restructuring costs over the course of 2018. In connection with our focus on maintaining positive **operating leverage**, we will likely incur additional restructuring costs in the future. See note 10 “Other Operating Expenses” to our consolidated financial statements in Part II of this Form 10-K for additional information about our restructuring and cost savings initiatives. Interest Expense As a result of our capit...

### 8. TRI Pointe Homes, Inc.  (TPH)  (CIK 0001561680) - 10-K 2015-03-12 - `tph-10k_20141231.htm` -> **(a) / realized**
SIC 1531; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1561680/000156459015001605/tph-10k_20141231.htm)

*Why:* MD&A: G&A/revenue fell mainly on greater operating leverage from higher prices.

> ... and marketing expenses, with no comparable amounts in the prior year period. General and administrative expense decreased to 5.0% of home sales revenue for the year ended December 31, 2014 from 6.1% of home sales revenue for the same period in the prior year. The decrease was mainly due to greater **operating leverage** as a result of the 28% increase in the average sales prices of homes delivered during the year ended December 31, 2014, primarily as a result of the addition of legacy TRI Pointe, along with higher average selling prices across all of our existing segments. General and administrative expenses incre...

### 9. SENIOR HOUSING PROPERTIES TRUST  (DHC, DHCNI, DHCNL)  (CIK 0001075415) - 10-K 2011-02-24 - `a2201648z10-k.htm` -> **(c) / risk-factor**
SIC 6798; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1075415/000104746911001263/a2201648z10-k.htm)

*Why:* Item 1A risk factor (healthcare REIT, SIC 6798) about a tenant: 'Five Star has high operating leverage'.

> ...has access to a revolving line of credit from a financial institution for $35.0 million maturing in March 2013, Five Star has limited resources and has substantial lease obligations to us and others. Five Star's business is subject to a number of risks, including the following: • Five Star has high **operating leverage**. A small percentage decline in Five Star's revenue or increase in Five Star's expenses could have a material negative impact on Five Star's operating results; • Medicare and Medicaid payments account for some of Five Star's total revenues. A reduction in these payment rates or a failure of these pa...

### 10. ALLIANCEBERNSTEIN L.P.  (CIK 0001109448) - 10-K 2023-02-10 - `ablp-20221231.htm` -> **(d) / financial**
SIC 6282; doc_role=main; earnings 8-K=False; occurrences in file=2; [link](https://www.sec.gov/Archives/edgar/data/1109448/000110944823000013/ablp-20221231.htm)

*Why:* Asset manager (SIC 6282): drive operating leverage on incremental revenues; compensation-ratio discussion.

> ...adquarters from New York City to Nashville. In 2022, we continued to relocate positions to our recently constructed Nashville headquarters. We have relocated over 85% of our targeted 1,250 positions. We continue to seek efficiencies and manage various operating expenses to help ensure that we drive **operating leverage** on incremental revenues. Declines in equity and fixed income markets in 2022 negatively impacted our revenues, resulting in a rolling three-year incremental adjusted operating margin of 35%, below our targeted range of 45% to 50%. Our adjusted operating margin decreased to 28.4% in 2022, down 520 b...

> ...e $ 1,613,282 Adjusted Compensation Ratio 48.4 % Our 2022 adjusted compensation ratio of approximately 48.4% reflects a balancing of the need to keep compensation levels competitive with industry peers in order to attract, motivate and retain highly-qualified talent with the need to maintain strong **operating leverage** in our business. The Compensation Committee works with management to help ensure both needs are sufficiently addressed. 132 AllianceBernstein Table of Contents Part III We have described below each NEO’s individual achievements in 2022 given each officer’s role, the contents of their respective per...

### 11. Freescale Semiconductor Holdings I, Ltd.  (CIK 0001392522) - 10-K 2012-02-03 - `d270544d10k.htm` -> **(a) / realized**
SIC 3674; doc_role=main; earnings 8-K=False; occurrences in file=3; [link](https://www.sec.gov/Archives/edgar/data/1392522/000119312512038997/d270544d10k.htm)

*Why:* MD&A gross margin: higher fab utilization improved operating leverage of fixed manufacturing costs (section heuristic said risk factors; wrong).

> ...ued at the lower of cost or estimated net realizable value. Gross Margin Our gross margin is significantly influenced by our utilization. Utilization refers only to our wafer fabrication facilities and is based on the capacity of the installed equipment. As utilization rates increase, there is more **operating leverage** because fixed manufacturing costs are spread over higher output. We experienced a moderate increase in our utilization rate to 80% in the fourth quarter of 2011 compared to 75% in the fourth quarter of 2010. We also experienced a significant increase in our utilization rate to 75% in the fourth qua...

> ...ulting from a change in the useful lives of certain of our probe, assembly and test equipment in the first quarter of 2011. The improvement in wafer manufacturing facility utilization (from 72% in 2010 to 77% for 2011) and the decrease in depreciation expense contributed to continued improvement in **operating leverage** of our fixed manufacturing costs. Partially offsetting these improvements in gross margins were decreases in average selling price resulting from our annual negotiations with our customers put into effect in the first quarter of 2011 and changes in product sales mix. Our gross margin included PPA i...

> ...table to higher net sales and an increase in factory utilization of approximately 15 percentage points as compared to the end of 2009. The increase in factory utilization and a $112 million decrease in depreciation and amortization expense positively impacted gross margin, as we experienced greater **operating leverage** of our fixed manufacturing costs. In addition, in connection with increasing our capacity to meet current demand, our manufacturing and supply chain operations workforce increased 13% from the end of 2009 to the end of 2010. Manufacturing-related expenses, including tool maintenance and support, pu...

### 12. Tavia Acquisition Corp.  (TAVI, TAVIR, TAVIU)  (CIK 0002020385) - 10-K 2025-03-31 - `ea0235838-10k_tavia.htm` -> **(c) / boilerplate**
SIC 6770; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/2020385/000121390025026416/ea0235838-10k_tavia.htm)

*Why:* SPAC (SIC 6770) target-selection criteria boilerplate (same text as sample 6).

> ... We intend to seek to acquire one or more businesses that have the potential for significant revenue and earnings growth through a combination of both existing and new product development, increased production capacity, expense reduction and synergistic follow-on acquisitions resulting in increased **operating leverage**. ● Potential for Strong Free Cash Flow Generation. We intend to prioritize targets with a demonstrable track record of robust and sustainable free cash flow, or the potential to achieve it in the near future. ● Benefit from Being a Public Company. We intend to acquire a business or businesses that ...

### 13. CHOICE HOTELS INTERNATIONAL INC /DE  (CHH)  (CIK 0001046311) - 10-K 2016-02-29 - `chh1231201510-k.htm` -> **(a) / forward**
SIC 7011; doc_role=main; earnings 8-K=False; occurrences in file=5; [link](https://www.sec.gov/Archives/edgar/data/1046311/000104631116000023/chh1231201510-k.htm)

*Why:* Business section: continued franchise growth should let us realize benefits from the operating leverage in place; also industry description.

> ...rate realized. Our variable overhead costs associated with franchise system growth of our established brands have historically been less than incremental royalty fees generated from new franchises. Accordingly, continued growth of our franchise business should enable us to realize benefits from the **operating leverage** in place and improve operating results. We are contractually required by our franchise agreements to use the marketing and reservation system fees we collect for system-wide support activities. These expenditures help to enhance awareness and increase consumer preference for our brands. Greater awa...

> ...ip requires a substantial capital commitment and involves the most risk but offers high returns due to the owner’s ability to influence margins by driving RevPAR, managing operating expenses and financial leverage. The ownership model has a high fixed-cost structure that results in a high degree of **operating leverage** relative to RevPAR performance. As a result, profits escalate rapidly in a lodging up-cycle but erode quickly in a downturn as costs rarely decline as fast as revenue. Profits from an ownership model increase at a greater rate from RevPAR growth attributable to average daily rate ("ADR") growth, th...

> ...-revenue royalty fee and a marketing/reservation fee. A franchisor’s revenues are dependent on the number of rooms in its system and the top-line performance of those hotels. Earnings drivers include RevPAR increases, unit growth and effective royalty rate improvement. Franchisors enjoy significant **operating leverage** in their business model since it typically costs little to add a new hotel franchise to an existing system. Franchisors normally benefit from higher industry supply growth, because unit growth usually outpaces lower RevPAR resulting from excess supply. As a result, franchisors benefit from both Rev...

### 14. CAMPBELL SOUP CO  (CPB)  (CIK 0000016732) - 10-K 2023-09-21 - `cpb-20230730.htm` -> **(e) / ambiguous**
SIC 2000; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/16732/000001673223000109/cpb-20230730.htm)

*Why:* Footnote to a gross-margin bridge: '(2) Includes the impact of operating leverage' - direction not stated.

> ...30 basis points from the benefit of cost savings initiatives, which was more than offset by cost inflation and other factors, including a 130 basis-point negative impact from the change in unrealized mark-to-market adjustments on outstanding undesignated commodity hedges. (2) Includes the impact of **operating leverage**. Marketing and Selling Expenses Marketing and selling expenses as a percent of sales were 8.7% in 2023, 8.6% in 2022 and 9.6% in 2021. Marketing and selling expenses increased 10% in 2023 from 2022. The increase was primarily due to higher advertising and consumer promotion expense (approximately 7...

### 15. Founder SPAC  (RBTC, RBTCW)  (CIK 0001862068) - 10-K 2022-03-29 - `founderspac_10k.htm` -> **(c) / boilerplate**
SIC 7372; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1862068/000182912622006864/founderspac_10k.htm)

*Why:* SPAC with a software SIC (7372): target criteria boilerplate - slips past the SIC 6000-6999 screen.

> ...r decision-making framework. These metrics include, but are not limited to, revenue and annual recurring revenue growth, customer and revenue retention rates (both gross and net), and gross profit margin. We believe targets developing transformative solutions and exhibiting low customer churn, high **operating leverage**, and outsized growth potential present compelling target candidates. 4 These criteria are not intended to be exhaustive. Any evaluation related to the merits of an initial business combination may be based, to the extent relevant, on these generic guidelines as well as other considerations, factors...

### 16. National General Holdings Corp.  (CIK 0001578735) - 10-K 2021-02-26 - `nghc-20201231.htm` -> **(d) / financial**
SIC 6331; doc_role=main; earnings 8-K=False; occurrences in file=4; [link](https://www.sec.gov/Archives/edgar/data/1578735/000157873521000032/nghc-20201231.htm)

*Why:* Insurer (SIC 6331): operating leverage = net earned premium / equity (insurance-industry meaning).

> ...vere or inclement weather. Our operating results for the year ended December 31, 2020, have been negatively impacted by losses resulting from severe weather-related events. We evaluate our operations by monitoring key measures of growth and profitability, including net combined ratio (non-GAAP) and **operating leverage**. We target a net combined ratio (non-GAAP) in the low-to-mid 90s while seeking to maintain optimal **operating leverage** in our insurance subsidiaries commensurate with our A.M. Best rating objectives. To achieve our targeted net combined ratio (non-GAAP) we continually seek ways to reduce our operati...

> ...to maintain optimal **operating leverage** in our insurance subsidiaries commensurate with our A.M. Best rating objectives. To achieve our targeted net combined ratio (non-GAAP) we continually seek ways to reduce our operating costs and lower our expense ratio. For the year ended December 31, 2020, our **operating leverage** (the ratio of net earned premium to average total stockholders’ equity) was 1.5x, which was within our planned target **operating leverage** of between 1.5x and 2.0x. Investment income is also an important part of our business. Because we often do not settle claims until several months or longer after ...

### 17. Shake Shack Inc.  (SHAK)  (CIK 0001620533) - 10-K 2024-02-29 - `shak-20231227.htm` -> **(c) / risk-factor**
SIC 5810; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1620533/000162053324000023/shak-20231227.htm)

*Why:* Item 1A risk factor: new-market Shacks may have reduced operating leverage.

> ...ay also incur higher costs from entering new markets if, for example, we assign area directors to manage comparatively fewer Shacks than we assign in more developed markets. Also, until we attain a critical mass in a market, the Shacks we do open may incur higher food distribution costs and reduced **operating leverage**. As a result, these new Shacks may be less successful or may achieve target Shack-level operating profit margins at a slower rate, if ever. If we do not successfully execute our plans to enter new markets, our business, financial condition or results of operations could be adversely affected. Our f...

### 18. VALSPAR CORP  (CIK 0000102741) - 10-K 2011-12-21 - `valspar114699_10k.htm` -> **(a) / realized**
SIC 2851; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/102741/000089710111002144/valspar114699_10k.htm)

*Why:* MD&A: segment EBIT decline partly offset by operating leverage on higher net sales.

> ...ween higher raw material costs and selling price increases, restructuring charges, a net gain on the sale of certain assets recognized in 2010 of $11,497 or 0.5% of net sales and acquisition-related charges of $1,859 or 0.1% of net sales in 2011. The decline was partially offset by new business and **operating leverage** on higher net sales. The restructuring charges for 2011 and 2010 periods were $20,940 or 1.0% of net sales and $10,563 or 0.6% of net sales, respectively. 15 Table of Contents • Paints Segment EBIT – EBIT as a percent of net sales decreased primarily due to the lag between higher raw material costs...

### 19. PROSPER MARKETPLACE, INC  (CIK 0001416265) - 10-K 2022-03-28 - `prosper-20211231.htm` -> **(d) / financial**
SIC 6199; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1416265/000141626522000167/prosper-20211231.htm)

*Why:* Online lender (SIC 6199) business description: platform provides significant operating leverage.

> ...rrower Loans and Loans Held for Sale, credit referral fees and other ancillary revenue sources. Additionally, our technology platform significantly reduces the need for physical infrastructure and therefore allows our business to grow with a lower cost operating model, providing us with significant **operating leverage**. Sources of Revenues We have three primary sources of personal loan revenues: transaction fees, servicing fees, and net interest income. We earn transaction fees from WebBank by facilitating the origination of Borrower Loans through the personal loan marketplace, and we earn servicing fees from inv...

### 20. CBOE Holdings, Inc.  (CBOE)  (CIK 0001374310) - 10-K 2011-03-16 - `a2202482z10-k.htm` -> **(d) / financial**
SIC 6200; doc_role=main; earnings 8-K=False; occurrences in file=1; [link](https://www.sec.gov/Archives/edgar/data/1374310/000104746911002202/a2202482z10-k.htm)

*Why:* Exchange operator (SIC 6200): managing expense growth to drive greater operating leverage (same text as sample 5, 2011 10-K).

> ...ved from fines assessed for rule violations; and • Other sources of revenue. Components of Operating Expenses Most of our expenses do not vary directly with changes in our trading volume except royalty fees and trading volume incentives. We remain focused on managing expense growth to drive greater **operating leverage** and continue to explore opportunities to expand our margins. Employee Costs Employee costs is our most significant expense and includes employee wages, stock-based compensation, bonus expense, benefits and employer taxes. Salaries and benefits represent our largest expense category and tend to be d...
