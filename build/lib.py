# Starter rules and skills: one source for both the app's built-in copies and the files in the folder.
RULES = [
("01-document-structure.md", """# Document structure

How every report and update is organised.

## Do
- Open with a title of at most 8 words that names the subject and the place.
- Put a **Summary** of 3 to 5 bullet points first, so a busy reader can stop there.
- Follow with sections in this order where they apply: background, how it works, findings, options, costs, risks, recommended next steps.
- End every report with **Recommended next steps** as a numbered list, most urgent first.
- Give each section one job, and say the most important thing in its first sentence.
- State the date of the information and the exchange rate used, once.

## Don't
- Don't open with an introduction about what the document will cover.
- Don't repeat the summary in a conclusion.
- Don't bury a decision or a warning in the middle of a paragraph.
- Don't add a section that has nothing specific to say.
"""),
("02-formatting-and-style.md", """# Formatting and style

How the text itself should read.

## Do
- Write in plain English, in short sentences, in the active voice.
- Use the reader's own terms, and define any technical term the first time it appears.
- Use bullet points for lists of separate items, and numbered lists for steps in order.
- Start each bullet with a short bold label when the list has more than four items.
- Give amounts in local currency first, with the US dollar equivalent in brackets.
- Write numbers with units, and ranges with both ends (for example Kshs 6,000 to 9,500 per metre).

## Don't
- Don't use filler such as "it is important to note" or "in today's world".
- Don't use jargon, slang or abbreviations the reader has not been given.
- Don't write paragraphs longer than five lines.
- Don't use capital letters or exclamation marks for emphasis.
- Don't hedge every sentence; say once how sure the finding is.
"""),
("03-sources-and-figures.md", """# Sources and figures

How facts are supported and how doubt is shown.

## Do
- Name the source of each key fact or figure in the sentence that states it.
- Prefer official and primary sources: regulators, government gazettes, standards bodies, company filings.
- Say plainly when a figure is an estimate, and whose estimate it is.
- Flag anything that could not be verified, and say what would confirm it.
- When sources disagree, give both figures and say which is more likely to be right, and why.
- Check the date of every source, and say so when the newest one found is old.

## Don't
- Don't invent a source, a figure, a name or a link.
- Don't present a seller's marketing page as an independent fact.
- Don't round an uncertain figure into a confident one.
- Don't leave out a risk because it weakens the recommendation.
"""),
("04-visuals-and-tables.md", """# Visuals and tables

When to draw, tabulate or show a photo.

## Do
- Draw a flow chart whenever a process has three or more steps.
- Draw a block diagram when a system has parts that feed one another.
- Put comparisons and figures in a table, with units in the column headings.
- Keep a diagram to 12 boxes or fewer, with short labels.
- Write one or two sentences under every diagram, table and photo saying what it shows and why it matters.
- Use a photo only where seeing the real thing helps the reader recognise or choose it.

## Don't
- Don't add a diagram that only repeats the headings of the document.
- Don't put more than six columns in a table.
- Don't leave a visual without an explanation.
- Don't use a visual in place of a figure the reader needs in words.
"""),
]
SKILLS = [
("feasibility-study", """---
name: Feasibility study
description: Tests whether a business or project idea is worth doing in the user's country, with costs, demand, rules and a go or no-go view.
---

# Feasibility study

## When to use
The user has an idea for a business, product or project and wants to know if it can work before spending money.

## Steps
1. Restate the idea in one sentence: what is sold, to whom, and where.
2. Size the demand: who buys now, how many, and what they pay. Name the source of each number.
3. List the competition and what each charges.
4. Set out the rules: registration, licences, permits and taxes, with the body responsible for each.
5. Estimate start-up costs and monthly running costs as ranges, in local currency with US dollars in brackets.
6. Build a simple break-even: price, cost per sale, fixed costs, and the sales needed each month.
7. List the main risks and one way to reduce each.
8. Give a clear view: go, go with conditions, or do not go, and the one fact that would change that view.

## Output
- Summary, then sections in the order of the steps above.
- One table for costs and one for the break-even.
- One flow chart from first customer contact to first payment.
- Recommended next steps for the first 30 days.

## Checks before finishing
- Every cost has a source or is marked as an estimate.
- The break-even arithmetic adds up.
- The view at the end follows from the figures.
"""),
("tender-bid-review", """---
name: Tender and bid review
description: Reads a tender or request for proposals and produces a bid or no-bid brief with requirements, deadlines, risks and a compliance checklist.
---

# Tender and bid review

## When to use
The user is a contractor or consultant deciding whether to bid for a tender, or preparing a bid.

## Steps
1. Identify the buyer, the reference number, the scope, the estimated value and the closing date and time.
2. List the mandatory requirements: registration, tax compliance, licences, bid security, experience and key staff.
3. List the evaluation criteria and the weight of each, where they are published.
4. Check eligibility: reserved categories, joint venture rules, local content rules.
5. Set out the timeline from clarification deadline to contract award.
6. Flag the risks: payment terms, penalties, unclear scope, short deadlines, and anything unusual.
7. Recommend bid or no-bid, with the three reasons that matter most.

## Output
- Summary with the closing date in the first bullet.
- A compliance checklist as a table: requirement, document needed, have it or not.
- A flow chart of the bid timeline.
- Recommended next steps with an owner and a date for each.

## Checks before finishing
- The closing date, time and submission method are stated exactly as published.
- Nothing is marked as verified unless it came from the tender documents or the buyer.
- Posts that look fake are flagged: no reference number, a fee to apply, a personal email address.
"""),
("job-search-brief", """---
name: Job search brief
description: Finds current job openings that fit the user's background, weeds out doubtful postings and ranks the rest with what to do for each.
---

# Job search brief

## When to use
The user is looking for work, or wants to know what roles are open for someone with their experience.

## Steps
1. State the profile being matched: field, years of experience, location, and any limits the user gave.
2. Search for openings posted in the last 30 days. Record the employer, title, location, closing date and where it was posted.
3. Check each posting: does the employer exist, is the posting on the employer's own site, and is there any request for money.
4. Drop or flag doubtful postings, and say why.
5. Score the rest against the profile: strong match, partial match or stretch.
6. For each strong match, name the two requirements the user should speak to first.

## Output
- Summary with the number of openings found and the best three.
- A table: role, employer, location, closing date, match, source.
- A short note per strong match on how to apply.
- Recommended next steps for the coming week.

## Checks before finishing
- Every opening has a closing date or is marked "no date given".
- No posting that asks for a fee is recommended.
- Salary figures are given only where a source states them.
"""),
("technical-explainer", """---
name: Technical explainer
description: Explains how a technology, system or method works at the user's chosen level, with a diagram and a worked example.
---

# Technical explainer

## When to use
The user wants to understand how something works, not to decide whether to buy or build it.

## Steps
1. Say in one sentence what the thing does and why anyone uses it.
2. Name the main parts and what each one does.
3. Walk through how it works, step by step, in the order things happen.
4. Give one worked example with real numbers and units.
5. State the limits: when it does not work well, and the common mistakes.
6. Point to what to learn next.

## Output
- Summary, then the parts, then how it works.
- One block diagram of the parts and one flow chart of the steps.
- The worked example in its own section, with the arithmetic shown.
- A short glossary if more than five technical terms were needed.

## Checks before finishing
- A reader at the chosen level could explain it back.
- The worked example can be checked with a calculator.
- Every formula says what each symbol means and its unit.
"""),
]

SKILLS.append(("business-idea-presentation", """---
name: Business idea presentation
description: Researches a business idea and builds a 20-slide pitch presentation that downloads as a PowerPoint file.
output: presentation
---

# Business idea presentation

## When to use
The user wants to present a business idea to investors, partners, a bank or a board, and needs slides, not a report.

## Slides, in this order
Each line gives the slide, its layout, and what it must contain.

1. **Title** (title): the business name or idea in at most 6 words, and a one-line promise.
2. **Company overview** (panel, with a photo): who we are, what we do, and for whom, in at most 45 words.
3. **Problem** (text, with a photo): the problem, who has it, and what it costs them. One sourced figure.
4. **Solution** (steps): three steps or parts that show how the idea solves the problem.
5. **How it works** (steps): the customer's path from first contact to payment, in 4 or 5 steps.
6. **Market opportunity** (stats): three or four numbers: market size, growth, and the share within reach. Name the source.
7. **Target customer** (text, with a photo): the first customers to win, where they are, and how they buy.
8. **Business model canvas** (grid, 9 boxes): key partners, key activities, key resources, value proposition, customer relationships, channels, customer segments, cost structure, revenue streams.
9. **Revenue model** (steps): how money comes in, from who pays to how often, in 4 or 5 steps.
10. **Pricing** (table): products or plans, price, and what is included.
11. **Competitive landscape** (table): three to five competitors compared on price, strength and weakness.
12. **Competitive advantage** (panel): the two or three things that are hard to copy.
13. **Go-to-market** (text): the channels and first 90 days of selling.
14. **Traction and validation** (stats): what is already proven: customers, pilots, sign-ups, letters of intent. Say plainly if there is none yet.
15. **Roadmap** (steps): four or five milestones with dates.
16. **Team** (grid): the people or roles, and what each brings.
17. **Financial projections** (table): three years of revenue, costs and profit. Mark estimates as estimates.
18. **Funding and use of funds** (table): the amount sought and what it will be spent on, with percentages.
19. **Risks** (grid): four to six risks, each with how it is reduced.
20. **Next steps** (close): the ask, the decision wanted, and contact details.

## Writing rules for slides
- One idea per slide. A title of at most 6 words that states the point.
- At most 45 words of body text, or 5 bullets of at most 12 words each.
- Numbers carry their unit and their source.
- Money in local currency with US dollars in brackets.
- Speaker notes for every slide: one to three sentences on what to say.
- Leave out a slide only if nothing true can be said on it, and say so in the notes of the slide before.

## Look
- Wide 16:9 slides on a dark background, with a light slide every few slides for contrast.
- Serif titles, plain sans-serif body, one accent colour, and generous empty space.
- Photos on overview, problem and customer slides only; diagrams and tables carry the rest.

## Checks before finishing
- All 20 slides are present and in order.
- Every figure has a source or is marked as an estimate.
- The financial table adds up, and the funds table totals 100%.
"""))
