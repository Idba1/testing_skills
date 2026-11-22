# বাংলায় সহজে প্রজেক্টটি ব্যবহার করার নির্দেশনা

## কাজটা কী?
এই assignment-এ একই ধরনের testing task বারবার করার জন্য **৭টি reusable AI skill** তৈরি করা হয়েছে। প্রতিটি skill-এর আলাদা `SKILL.md` আছে। সেখানে সাতটি section রয়েছে: Input, Processing Logic, Instructions, Tools, Output, Validation, Failure Handling। এগুলো শুধু prompt নয়; prompt কীভাবে ব্যবহার, যাচাই এবং ভুল হলে কী করব সেটাও লেখা আছে।

## কোন skill কী করে?
1. **Requirement Ambiguity Analyser** — unclear requirement থেকে প্রশ্ন বের করে।
2. **Test Case Generator with Coverage Constraints** — requirement অনুযায়ী positive/negative/boundary test case design করে; integer-boundary helper আছে।
3. **Coverage Gap Auditor** — কোন requirement-এর কোন ধরনের test আছে বা নেই, তার structural report দেয়।
4. **Automation Code Reviewer** — automation code-এ weak assertion, fragile locator ইত্যাদি review করার instruction দেয়।
5. **Workload Model Builder** — session arrivals, duration, requests/session থেকে illustrative performance load হিসাব করে।
6. **Threat Model Generator** — architecture-এ সম্ভাব্য security risks/STRIDE categories নিয়ে candidate list বানানোর instruction দেয়।
7. **Nine-Dimension Output Evaluator** — Week 10-এর ৯টি exact dimension ধরে AI-generated QA artifact evaluate করার প্রক্রিয়া দেয়; script শুধু review record পূর্ণ কি না পরীক্ষা করে।

## Windows-এ কীভাবে চালাবে?
1. ZIP Extract করো।
2. Extract করা `qa-testing-skills` folder ওপেন করো।
3. File Explorer-এর address bar-এ `cmd` লিখে Enter দাও।
4. Python installed আছে কি না: `python --version` অথবা `py --version`। Python install না থাকলে Python 3.9+ setup করতে হবে।
5. Test চালাও: `python verification/run_tests.py`। (প্রয়োজনে `python`-এর জায়গায় `py`।)
6. Coverage example দেখাতে:

```bat
python coverage-gap-auditor/scripts/coverage_audit.py --requirements coverage-gap-auditor/examples/requirements.csv --tests coverage-gap-auditor/examples/tests.csv --output coverage-gap-auditor/examples/coverage_report.json
```

7. তৈরি হওয়া JSON ফাইল Notepad/VS Code দিয়ে খুলে দেখো। অন্য ৩টি script-এর command মূল `README.md`-এ আছে।

## স্যারকে কীভাবে explain করবে?
"আমি Week 12-এর ৭টি candidate reusable skill নিয়েছি। প্রতিটির Input, Processing Logic, Instructions, Tools, Output, Validation, Failure Handling আলাদা করেছি। চারটিতে narrowly scoped Python script আছে, বাকি তিনটি instruction-based। Python scripts synthetic data দিয়ে চালিয়ে test করেছি। Week 10-এর ৯টি evaluation dimension একই নামে ব্যবহার করেছি। Script pass মানে কোনো production app test করা হয়েছে এমন দাবি নয়; AI judgement-এর পরে human review প্রয়োজন।"

## Submission-এর আগে মনে রাখবে
Working brief অফিসিয়াল assignment নয়। স্যার যদি অন্য submission format, specific script count বা mark distribution দেন, সেই requirements অনুযায়ী project update করতে হবে। `SUBMISSION_CHECKLIST.md`-এ কোনগুলো নিশ্চিত নয় লেখা আছে।
