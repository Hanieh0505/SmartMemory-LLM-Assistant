from openai import OpenAI
from dotenv import load_dotenv
import os
from transformers import AutoTokenizer


class ChatBot:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GROQ_API_KEY')
        self.base_url='https://api.groq.com/openai/v1'
        self.messages = [
            {'role':'system','content':'you are a helpful assistant . give a short answers and be kind'},
        ]
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0


        self.iteration = 0

        self.tokenizer =AutoTokenizer.from_pretrained('Qwen/Qwen2.5-7B-Instruct')

    def history_masseges(self, max_history=6):
        system_message = [m for m in self.messages if m['role'] == "system" ]
        other_messages = [m for m in self.messages if m['role'] != 'system']

        if len(other_messages) > max_history:
            other_messages = other_messages[-max_history:]
            self.messages = [*system_message, *other_messages]

    def summarize_messages(self):
        if self.iteration % 5 != 0 or len(self.messages) < 6:
            return
        system_message = [m for m in self.messages if m['role'] == "system" ]
        other_messages = [m for m in self.messages if m['role'] != 'system']

        early_messages, last_messages = other_messages[0:4], other_messages[4:]

        try:
            llm= OpenAI(api_key=self.api_key, base_url=self.base_url)
            response = llm.chat.completions.create(
                model = 'openai/gpt-oss-20b',
                temperature=0.5,
                messages=[
                    {
                    'role':'system',
                    'content':(
                        'Summarize these messages concisely, keeping key'
                        ' facts and informations'
                    ),},
                    *early_messages,
                ],
            )
            summarize_message = {
                'role': 'system',
                'content': (
                    'Summary of earlier conversation:'
                    f" {response.choices[0].message.content}"
                ),
            }
            self.messages = [
                *system_message,
                summarize_message,
                *last_messages,
            ]
            print('\n[system: Summarizatiion was successful]')
        except Exception as e:
            print(f'\n[System: Summarization failed: {e}]')

    def ask(self,message):


        self.messages.append(
            {'role':'user','content':message}
        )


        current_input_tokens = 0
        for msg in self.messages:
            current_input_tokens += len(self.tokenizer.encode(msg['content']))

        self.input_tokens += current_input_tokens
        self.total_tokens += current_input_tokens
        


        
        llm = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        response = llm.chat.completions.create(
            model='openai/gpt-oss-20b',
            temperature=0.5,
            stream=True,
            messages=self.messages
        )
        response_text = ""
        for chunk in response:

            if chunk.choices and chunk.choices[0].delta.content:

                delta = chunk.choices[0].delta.content
            
                print(delta, end='',flush=True)
                response_text += delta

        print()

        self.messages.append({'role':'assistant','content':response_text})


        bot_token_count = len(self.tokenizer.encode(response_text))
        self.output_tokens += bot_token_count
        self.total_tokens += bot_token_count


        self.history_masseges(max_history=6)

        self.summarize_messages()
        
        

    


    
    def chatting(self):
        print('ask anything you want :(for exit enter q ) ')
    
        while True:
            self.iteration += 1
            user_input = input('you : ').strip()



            if user_input.lower() == 'q':
                self.report()
                print('Good bye!')
                break
            if not user_input:
                continue

            token_count = len(self.tokenizer.encode(user_input))
            if token_count > 50:
                print(
                    'Your prompt exceeded the limit (50 tokens). Try a shorter'
                    ' one please.'

                )
                continue
            if self.total_tokens > 10_000:
                print(
                    'Unfortunately you exceeded the total token limit for today.'
                )
                self.report()
                break


            print('bot : ', end='')
            self.ask(user_input)
      
    def report(self):
        
            print('token usage ==> ')
            print(f"your input token's : {self.input_tokens}")
            print(f"your output token's : {self.output_tokens}")
            print(f"total tokens : {self.total_tokens}")     

if __name__ == '__main__':
    chatt = ChatBot()
    chatt.chatting()

