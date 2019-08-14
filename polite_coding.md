# Code Etiquette and Debugging

Writing a code is a useful skill once obtained and never lost. And more you code, better your skills are. But is it always a case?

Every additional line of code can make you train your skills. But it doesn't mean you are actually learning something new. So, even after 10 years of coding, you might still be on the baseline. What does actually define your growth as programmist? Only ***your** code* represents you. And if you don't follow **code etiquette**, you will not be appriciated.

First let's start with sove advices:

## 8 rules 

1. **Computer is never wrong**. Whenever you obtain an unsolveable error, take a break. "To take or not to take" - your computer knows better. 
2. **Calm down**. Emotions are bad. Obviously, it is difficult to concentrate on the code especially if it wasn't written by you. Calm down, think of it as a challenge. Take the challenge and be sure we believe in you.
3. **Just start**. No matter from which part of the task. No matter if it is a pseudocode generation or functional programming. Just start. You will never notice the moment when code is half-finished.
4. **Big Brother watches you**. You are creating a product (yeah, you will be paid for every line you write). Keep that in mind. Someone will read it after you. Make it as readable as possible. 
5. **Read books**. It is difficult to read books when your day is full of work/classes/whatever. But you need to grow as a personality, not onlyas a  professional. The main benefit of book reading is your ability to concentrate, imagine and discuss. 
6. **Know the tool you use**. *"I will never use it again"* is not an excuse to skip the documentation. Your code is automized as much as good you know the tool you use.
7. **No one is perfect**. If you spend most of your time trying to make your code perfect, you end up with no code. Try to keep is simple stupid on the develop step. And only when you make everything work, start optimizing and simplifying your code.
8. **Enjoy your free time**. If you think of the code all day long, you will dream of it as well. One can say it is good, but it is followed by overwork and exhausted brain. Exhausted brain can't solve problems. Have a hobby, go to gym, enjoy your life.



## Code etiquette [Zen of Python overview]

1. **Beautiful is better than ugly**. After dozens of hours spent for your code take a look on it again. Does every line of code looks readable? Does it looks elegant? Review your code before publishing.
2. **Explicit is better than implicit**. Have a proper naming for your variables. `g=k**2` tells nothing to you, while `variance=std**2` is understandable.
3. **Simple is better than complex**. Split your complex problem into lots of simple ones. Small wins and accomplishments are the best motivators.
4. **Complex is better than complicated**. If you didn't manage to get an array of simple problems - not a problem. Problem appears when you creat complicated solution for it. Remember to Keep It Simple Stupid and avoid unnecessary functions and steps. Let’s say my imaginary girlfriend asks me to make her a three-course meal for her birthday (:complex). Next, let’s instead say she asks me to take her to a restaurant she will enjoy (:complicated).
5. **Flat is better than nested**. Flat structure let you read your code with higher efficiency. You can easily say what is going with your variable or in which iteration you receive an error if your code is flat. 
6. **Sparse is better than dense**. Remember about intendation and keep space between different blocks of code. **NEVER** stick too much code on one line.
7. **Readability counts**. Respect your reader/viewer/reviewer. 
8. **Special cases aren't special enough to break the rules**. Keep in mind, no *except* is allowed to break your code. From other side, be consistant with general coding rules (keep in mind that someone not really familiar with Python might read your code).
9. **Although practicality beats purity**. Still sometimes exceptions from general rule are fine.
10. **Errors should never pass silently**. Never let errors, which may occur, confuse the reader. This may easily be resolved by printing a string when an error occurs.
11. **Unless explicitly silenced**. If you now about the error in the code, it should be well processed and not break the code. User should have the best experience - show that you are aware of this error by correct message.
12. **In the face of ambiguity, refuse the temptation to guess**. Never give a chance to interpret your code differently. If you give a choice to user, it should be guided choice, not random.
13. **There should be one-- and preferably only one --obvious way to do it**. Eliminate confusion. If you expect *DD-MM-YYYY* format of date as input, do not allow any other input formats.
14. **Now is better than never**. Even if better late then never, it is clearly better now then late. Do today what others won’t do. Do tomorrow what others can’t do.
15. **Although never is often better than *right* now**. It is always easy to overthink your problem. It is 11 pm and you just understood how to solve the problem you were thinking about for 12 hours? Write it down (don't forget about expliciteness) and go to bed. Writing something down later is often better than at this very moment giving your brain more time to think this solution over, but again, if we don’t do it now, the chances of it being done decreases.
16. **If the implementation is hard to explain, it's a bad idea**. Think twice before actualy running the code. Can't explain the solution to your grandmother? Okay, not grandma, but your groupmate - skip the solution. Or at least try to restructure it. Remember rules 3 and 4.
17. **If the implementation is easy to explain, it may be a good idea**. But anyway, some ideas are just bad, regardless of whether they are easy to implement or not.
18. **Namespaces are one honking great idea**. Classes are awesome. Once clearly defined, with all the rules and methods they become understandable for any user.

Import this library to your Python project to enjoy the poem.
```python
import this
```
