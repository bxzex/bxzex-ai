---
name: resume-job-apply
description: Tailoring a resume and short cover letter to a specific job posting, honestly and in plain ATS-friendly format.
---
# Resume and job applications

Never invent experience, titles, dates, degrees or numbers. Only reword and reorder what the user really has.

1. **Collect inputs.** Get the user's current resume (read_file) and the full job post (fetch_page or pasted text). If either is missing, ask.
2. **Pull keywords from the post.** List the required skills, tools, responsibilities and the exact words used (for example "stakeholder reporting", "Python", "inventory"). Mark which ones the user truly has. Those go in. The ones they lack stay out; mention them as a gap to the user.
3. **Structure, one page.**
   - Header: name, city, phone, email, one link (portfolio or profile). No photo, no full street address.
   - Summary: two lines, aimed at this role.
   - Experience, newest first: title, company, dates, 3 to 5 bullets each.
   - Skills: a plain comma-separated list using the post's wording.
   - Education and certifications, short.
4. **Write strong bullets.** Format: action verb, what you did, result. "Cut weekly report time from 6 hours to 2 by automating exports in Python." Use real numbers the user gives you (money, time, volume, team size). If there is no number, describe the scope honestly instead of making one up. Ask the user for figures.
5. **Format for parsers.** One column, standard headings (Experience, Education, Skills), a common font at 10 to 11pt, real bullet characters, no tables, text boxes, icons or images. Save as PDF unless the post asks for Word. Name it `FirstName-LastName-Resume.pdf` (see the documents skill).
6. **Cover letter, under 200 words, three short paragraphs.**
   - Why this company and role, with one specific detail about them.
   - Two achievements that match their top needs.
   - A plain closing with availability.
   Address a named person if the post gives one. No "I am writing to express my interest" and no list of buzzwords.
7. **Proofread.** Check spelling, tense (past for old jobs, present for current), consistent dates, and that the company name in the letter is the right one. Keep an untouched master copy and save each tailored version under a new name.

Tell the user what you changed and what gaps remain. Do not submit applications for them without being asked.
