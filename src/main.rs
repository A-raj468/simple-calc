use regex::Regex;

fn tokenize(s: &str) -> Vec<&str> {
    let mut tokens = vec![];
    let re = Regex::new(r"\d+|\+|\-|\*|\/|\%|\(|\)").unwrap();
    for mat in re.find_iter(s) {
        tokens.push(mat.as_str());
    }

    return tokens;
}

fn get_rpn(expr: &str) -> Vec<&str> {
    let tokens = tokenize(expr);

    fn precedence(op: &str) -> i32 {
        match op {
            "+" | "-" => 1,
            "*" | "/" | "%" => 2,
            _ => 0,
        }
    }

    let mut operands: Vec<&str> = vec![];
    let mut operators: Vec<&str> = vec![];

    for token in tokens {
        match token {
            "+" | "-" | "*" | "/" | "%" => {
                while !operators.is_empty()
                    && precedence(operators.last().unwrap()) >= precedence(token)
                {
                    operands.push(operators.pop().unwrap());
                }
                operators.push(token);
            }
            "(" => operators.push(token),
            ")" => {
                while !operators.is_empty() && *operators.last().unwrap() != "(" {
                    operands.push(operators.pop().unwrap());
                }
                operators.pop();
            }
            _ => operands.push(token),
        }
    }
    while !operators.is_empty() {
        operands.push(operators.pop().unwrap());
    }
    return operands;
}

fn evaluate(s: &str) -> i32 {
    let rpn = get_rpn(s);
    let mut stack: Vec<i32> = vec![];
    for token in rpn {
        match token {
            "+" => {
                let a = stack.pop().unwrap();
                let b = stack.pop().unwrap();
                stack.push(a + b);
            }
            "-" => {
                let a = stack.pop().unwrap();
                let b = stack.pop().unwrap();
                stack.push(b - a);
            }
            "*" => {
                let a = stack.pop().unwrap();
                let b = stack.pop().unwrap();
                stack.push(a * b);
            }
            "/" => {
                let a = stack.pop().unwrap();
                let b = stack.pop().unwrap();
                stack.push(b / a);
            }
            "%" => {
                let a = stack.pop().unwrap();
                let b = stack.pop().unwrap();
                stack.push(b % a);
            }
            _ => stack.push(token.parse::<i32>().unwrap()),
        }
    }
    return stack[0];
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tokenize() {
        assert_eq!(tokenize("3 + 4 * 2"), vec!["3", "+", "4", "*", "2"]);
        assert_eq!(
            tokenize("3 * (4 + 2)"),
            vec!["3", "*", "(", "4", "+", "2", ")"]
        );
        assert_eq!(
            tokenize("3 + 4 * 2 / (1 - 5) % 2"),
            vec!["3", "+", "4", "*", "2", "/", "(", "1", "-", "5", ")", "%", "2"]
        );
    }

    #[test]
    fn test_get_rpn() {
        assert_eq!(get_rpn("3+4*2"), vec!["3", "4", "2", "*", "+"]);
        assert_eq!(get_rpn("3*(4+2)"), vec!["3", "4", "2", "+", "*"]);
        assert_eq!(
            get_rpn("3+4*2/(1-5)%2"),
            vec!["3", "4", "2", "*", "1", "5", "-", "/", "2", "%", "+"]
        );
    }

    #[test]
    fn test_evaluate() {
        assert_eq!(evaluate("3+4*2"), 11);
        assert_eq!(evaluate("3*(4+2)"), 18);
        assert_eq!(evaluate("3+4*2/(1-5)%2"), 3);
    }
}

fn main() {
    let expression = "1 + 2 * 3";
    let value = evaluate(expression);
    println!("{:?}", value);
}
