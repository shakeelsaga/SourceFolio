# Testing Log

## Notes
- This log tracks the behavior of the system with various keyword inputs.

## Keyword Test Cases

| Test Case             | Expected Behavior                                     | Observed Behavior                                     | Example keywords                   | Pass/Fail |
|-----------------------|-------------------------------------------------------|-------------------------------------------------------|------------------------------------|-----------|
| Valid Keyword         | System recognizes the keyword and executes correctly  | System recognized the keyword and executed correctly  | elon musk, artificial intelligence | Pass      |
| Ambiguous Keyword     | System prompts for clarification or selects default   | System prompted for clarification                     | python, mercury                    | Pass      |
| Ambiguous Keyword     | System prompts for clarification or selects default   | System fetched default data                           | c (language/letter)                | Neutral   |
| Gibberish Keyword     | System returns an error or ignores the input          | System returned an error                              | hgacjhgs, blaba                    | Pass      |
| Misspelling Keywords  | System returns an error or asks for clarification     | System returns an error or asks for clarification     | pythn                              | Pass      |
| Misspelling Keywords  | System returns an error or asks for clarification     | System successfully fetches correct data              | gooogle                            | Pass      |
| Special Characters    | System sanitizes input and handles special characters | System successfully processes sanitized input         | #AI, c++                           | Pass      |
| Invalid Input         | System returns an error or ignores invalid inputs     | System returned an error                              | @@@, ###                           | Pass      |
| Disambiguation        | System prompts for clarification or selects default   | System prompted for clarification                     | mercury (planet vs element)        | Pass      |

## Additional Keyword Test Cases

| Keyword            | Expected Behavior                                                      | Observed Behavior                                                     | Pass/Fail |
|--------------------|------------------------------------------------------------------------|-----------------------------------------------------------------------|-----------|
| World War II       | System provides historical information about World War II              | System provides historical information about World War II             | Pass      |
| Diabetes           | System returns medical/health information about diabetes               | System returns medical/health information about diabetes              | Pass      |
| Stock Market       | System provides financial data or explanation about stock markets      | System provides financial data or explanation about stock markets     | Pass      |
| Amazon Rainforest  | System gives geographic/ecological info about the Amazon Rainforest    | System gives geographic/ecological info about the Amazon Rainforest   | Pass      |
| Shakespeare        | System returns biographical/literary info about Shakespeare            | System returns biographical/literary info about Shakespeare           | Pass      |
| Nobel Prize        | System explains or lists Nobel Prize details or history                | System explains or lists Nobel Prize details or history               | Pass      |
| Mars Rover         | System provides information about Mars rover missions                  | System provides information about Mars rover missions                 | Pass      |
| Olympics           | System returns data or history about the Olympic Games                 | System returns data or history about the Olympic Games                | Pass      |
| Van Gogh           | System provides information about the artist Vincent van Gogh          | System provides information about the artist Vincent van Gogh         | Pass      |
| Plastic Pollution  | System explains the concept and issues of plastic pollution            | System partially explains the concept and issues of plastic pollution | Neutral   |

## Note

Some queries may work in one API but fail in others (for example, `c++` may succeed in one but not another). We have recently added fixes to sanitize input and handle special characters properly to prevent crashes and improve consistency across different APIs. If you encounter test cases or discrepancies not listed here, feel free to fork this repository and update the test_log. You’re also welcome to open a pull request so I can review and merge your updates.
