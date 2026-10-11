# Control testing

This folder holds a control-testing programme I ran over this repository's own development controls. It doubles as an exercise in running AI agents under human oversight. An AI assistant, Claude Code, ran most of the test commands and drafted the workpapers and the memo under my direction, and it was not allowed to write or change any command output. I captured the GitHub evidence myself, made every ruling in the record and re-ran every command myself before publishing. I am new to control testing, and building this was how I learnt it.

This is not independent assurance. I built the repository and I tested it. The findings memo follows the conventions of ISAE 3000 and states that limitation in the terms an assurance practitioner would use.

There are ten controls: the checks meant to stop or catch a bad change before it reaches users, and to keep the legal rule data traceable to the law. Each was tested against a named practice or against what the repository itself states, and the control matrix cites every criterion. Every result has dated evidence in [`evidence/`](evidence/).

The testing produced four findings. Two are missing controls, both still open: no second person reviews a change before it reaches the main branch, and nothing makes a change wait for its tests. The other two are controls that did not work as claimed, and they rest on four conditions. Three were fixed during testing and are still reported: a rule that cited no provision, a README claim that every questionnaire question names a framework, and two install commands that failed. The fourth is still open: one legal statement sits in the code, although the README says all legal content sits in the data files.

Start with [`findings_memo.md`](findings_memo.md).
