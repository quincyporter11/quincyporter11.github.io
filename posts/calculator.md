---
title: "Python Calculator"
slug: "python-calculator"
date: "2025-10-17"
tags: ["python", "GUI"]
---

Here's a simple python calulator I created. It is split up into classes to keep everything nice and organized. I "borowed" some code for the calculate class evaluate function but it works pretty well as a one stop shop. This was also my first time using a loop to create all of the required buttons. There's always room for improvement but I think it turned out pretty well.

![Calculator](./calculator.png)


```python
import customtkinter

class Calculator():
    @staticmethod
    def evaluate(expression):
        try:
            expression = expression.replace("^", "**")
            result = eval(expression)
            return result
        except Exception:
            return "Error"

class ButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, textbox):
        super().__init__(master)
        self.textbox = textbox

        layout = [
            ["C", "⌫", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="]
        ]

        # for loop to create buttons based on layout
        for r, row in enumerate(layout):
            for c, text in enumerate(row):
                btn = customtkinter.CTkButton(
                    self,
                    text=text,
                    width=60,
                    height=50,
                    command=lambda t=text: self.on_button_click(t)
                )
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

        # Make layout responsive to window resize
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(len(layout)):
            self.grid_rowconfigure(i, weight=1)

    def on_button_click(self, char):
        current = self.textbox.get("1.0", "end-1c")

        if char == "C":
            self.textbox.delete("1.0", "end")
        elif char == "⌫":
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", current[:-1])
        elif char == "=":
            result = Calculator.evaluate(current)
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", str(result))
        elif char == "±":
            if current.startswith("-"):
                self.textbox.delete("1.0", "end")
                self.textbox.insert("1.0", current[1:])
            else:
                self.textbox.insert("1.0", "-")
        else:
            self.textbox.insert("end", char)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Python Calculator")
        self.geometry("320x450")

        self.textBox = customtkinter.CTkTextbox(self, width=250, height=50)
        self.textBox.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.buttonFrame = ButtonFrame(self, self.textBox)
        self.buttonFrame.grid(row=1, column=0, padx=10, pady=(10,0), sticky="nsew")

        # Make frame expand with window
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    app = App()
    app.mainloop()
```