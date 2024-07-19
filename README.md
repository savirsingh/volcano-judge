# Volcano Judge
### A minimalistic &amp; user-friendly competitive programming online judge.

Volcano Judge is an easy-to-use online judge and contest hosting system. You can see a live demo at https://volcanojudge.pythonanywhere.com.

Note that I built this judge as a learning project and it is not necessarily secure or efficient. However, it can be used by school clubs or small organizations looking for a simple solution to host fun programming competitions or events.

## Features
* Support for Python and C++.
  * Python is sandboxed and available by default for all problems.
  * C++ is not sandboxed/secure. It is available by default for contests and **Volcano Judge can compile & run C++ programs**, however, enabling C++ will make the system vulnerable to attacks.
* Easy-to-understand grading:
  * Simple & instantaneous feedback when users submit their code.
  * Enable custom checking & feedback on problems (e.g. a character limit on submissions for code golf style problems).
* Minimalistic Design:
  * Volcano Judge features a simple **Bootstrap-powered** design.
* Email Verification:
  * Built-in email verification for all users, via the admin's Gmail business account.
