import os
import ollama
from utils import count_tokens, get_sentences, overlapping_split
from dotenv import load_dotenv

from groq import Groq

ollama_models = {'mixtral:8x7b', ''}
groq_models = {'llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it'}
load_dotenv()


class SummaryAgent:
    def __init__(self, backend = 'groq', model_name="llama3-8b-8192"):
        self.model_name = model_name
        self.cache = {}
        self.backend = backend
        self.token_limit = 7500

        if backend == 'groq':
            self.groq_client = Groq(api_key=os.getenv("GROQ_API_TOKEN"))

    def __str__(self) -> str:
        s = f"SummaryAgent(model_name={self.model_name})"
        for key, value in self.cache.items():
            s += f"\n{key}: {value}"
        return s



    def get_completion(self, prompt, system_message= "You are a helpful assistant."):
        
        if self.backend == 'ollama':
                response = ollama.chat(
                        model='llama3:8b', 
                        messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt},        
                        ]
                    )
                return response['message']['content']
        elif self.backend == 'groq':
                chat_completion = self.groq_client.chat.completions.create(
                    model="llama3-8b-8192",
                        messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt},        
                        ]
                 )
                return chat_completion.choices[0].message.content
        else:
            raise ValueError("Please provide a valid inference: 'ollama' or 'groq'")
        
       
    def init_summary(self, prompt, system_message= "You are a helpful assistant."):
        
        print("   init_summary ....")
        system_message = "You are expert legal lawyer with European Court of Human Rights (ECHR)."

        user_prompt = f"""
            Could you please provide a summary of the given legal case, including all key points and supporting details?
            The summary should be comprehensive and accurately reflect the main and most important facts, procedure, and arguments presented in the original text,
            while also being concise and easy to understand. To ensure accuracy, please read the text carefully and pay attention to any nuances or complexities in the language.

            Do not provide any explanations or text apart from the summary.
            case: {prompt}
            Summary:       
         """
        response = self.get_completion(user_prompt, system_message)
        self.cache['summary'] = response 
        return response
    



    def reflect(self, source_text, summary):

        print("   reflect ....")
        system_message = "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        reflection_print = f"""
            Your task is to carefully read a source legal text and its legal summary, and then give constructive criticism and helpful suggestions to improve the summary. \
            The final style and tone of the summmary should match the style of legal text.

            The source text and initial summary, delimited by XML tags <SOURCE_TEXT></SOURCE_TEXT> and <SUMMARY></SUMMARY>, are as follows:

            <SOURCE_TEXT>
            {source_text}
            </SOURCE_TEXT>

            <SUMMARY>
            {summary}
            </SUMMARY>

            When writing suggestions, pay attention to whether there are ways to improve the summary's \n\
            (i) accuracy (by ensuring it correctly reflects the main points of the source text),\n\
            (ii) conciseness (by removing unnecessary details and repetitions),\n\
            (iii) clarity (by ensuring the summary is easy to understand),\n\
            (iv) coverage (by including all important aspects of the source text).\n\
            
            Write a list of specific, helpful and constructive suggestions for improving the summary.
            Each suggestion should address one specific part of the summary.
            Output only the suggestions and nothing else.
            
            Here is a list of suggestions:
        """
        response = self.get_completion(reflection_print, system_message)
        self.cache['reflection'] = response
        return response
        

    def improve(self, source_text, summary, reflection):
        
        print("   improve ....")
        system_message = "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        reflection_print = f"""
                Your task is to carefully read, then edit, a legal summary from {source_text} to {summary}, taking into
                account a list of expert suggestions and constructive criticisms.

                The source text, the initial summary, and the expert linguist suggestions are delimited by XML tags <SOURCE_TEXT></SOURCE_TEXT>, <SUMMARY></SUMMARY> and <EXPERT_SUGGESTIONS></EXPERT_SUGGESTIONS> \
                as follows:

                <SOURCE_TEXT>
                {source_text}
                </SOURCE_TEXT>

                <SUMMARY>
                {summary}
                </SUMMARY>

                <EXPERT_SUGGESTIONS>
                {reflection}
                </EXPERT_SUGGESTIONS>

                Please take into account the expert suggestions when editing the summary. Edit the summary by ensuring:

                (i) accuracy (by ensuring it correctly reflects the main points of the source text),
                (ii) conciseness (by removing unnecessary details and repetitions), \
                (iii) clarity (by ensuring the summary is easy to understand),
                (iv) coverage (by including all important aspects of the source text).

                Output only the new summary and nothing else.
                
                Here is the revised summary:
            """
        response = self.get_completion(reflection_print, system_message)
        self.cache['improvment'] = response
        return response
    
    def summarize(self, source_text):
         
        init_summary = self.init_summary(source_text)
        reflection = self.reflect(source_text, init_summary)
        improved_summary = self.improve(source_text, init_summary, reflection)

        return improved_summary
    
    def summarize_list(self, text_list):
        complete_summary = ''
        for text in text_list:
            complete_summary += self.summarize(text)
        return complete_summary


    def summarize_case(self, legal_case_dict):
        
        long_keys = ['procedure', 'law', 'facts', 'conclusion']
        summarized_legal_case = {}
        
        for key in legal_case_dict:
            if key in long_keys:
                print(f"Summarizing {key}")
                num_tokens = count_tokens(legal_case_dict[key])
                if num_tokens > self.token_limit:
                    overlapping_splits = overlapping_split(legal_case_dict[key])
                    summarized_legal_case[key] = self.summarize_list(overlapping_splits)
                else:
                    summarized_legal_case[key] = self.summarize(legal_case_dict[key])
            else:
                summarized_legal_case[key] = legal_case_dict[key]

        return summarized_legal_case
