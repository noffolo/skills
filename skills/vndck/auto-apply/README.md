# Auto-Apply - AI Job Search & Application Automation

Automate your entire job search and application process from your AI agent. Search thousands of jobs, tailor your resume to each role, track applications through your pipeline, and prepare everything so you only need to click apply.

## What it does

- **Smart job search** - Find job listings by keywords, location, remote preference, employment type, and more across thousands of sources
- **Resume tailoring** - Optimize your CV for each role based on the job description and your career profile using AI
- **Application tracking** - Save jobs to your tracker, update status as you progress through your pipeline, add notes and priority
- **Career profile** - Access your skills, work experience, and education to personalize job searches and recommendations
- **Auto-apply preparation** - Everything gets prepared so you only need to visit the apply link and click submit

## Getting an API key

1. Sign in to your Mokaru account at [mokaru.ai](https://mokaru.ai)
2. Go to **Settings > API Keys**
3. Create a new key with the scopes you need: `jobs:search`, `tracker:read`, `tracker:write`, `profile:read`
4. Copy the key (starts with `mk_`) and set it as `MOKARU_API_KEY` in your environment

## Example usage

```
> Find me remote React jobs in the US

Searching for "React" jobs, remote, in the US...
Found 47 results. Here are the top 5:

1. Senior React Engineer - Stripe (Remote, US) - $180k-$220k/yr
2. React Developer - Shopify (Remote) - $140k-$170k/yr
...

> Save the Stripe one to my tracker

Saved "Senior React Engineer" at Stripe to your application tracker.
Apply here: https://stripe.com/careers/1234

> I applied, mark it

Updated status to "applied".
```

## Use cases

```
> Tailor my resume for this job
> Help me prepare for my job search
> What jobs match my skills?
> Find me remote React jobs in Europe
> Save this job and optimize my CV for it
> Show my application pipeline
```

## Scopes reference

| Scope           | Endpoints                              |
|-----------------|----------------------------------------|
| `jobs:search`   | Search job listings                    |
| `tracker:read`  | List tracked applications              |
| `tracker:write` | Create and update tracked applications |
| `profile:read`  | Read career profile                    |

## Keywords

job search, auto apply, resume builder, resume tailor, CV optimization, application tracker, career coaching, job hunting, remote jobs, hiring, interview prep, job board, career management, AI recruiter, job matching

## Learn more

Full API documentation: [mokaru.ai/docs/api](https://mokaru.ai/docs/api)
