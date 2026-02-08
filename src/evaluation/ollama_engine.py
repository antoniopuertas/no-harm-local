"""Ollama inference engine for Non-Nocere evaluation framework"""
import ollama
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class OllamaEngine:
    """Inference engine using Ollama for local model execution"""
    
    def __init__(self):
        """Initialize Ollama engine"""
        self.loaded_models = {}
        logger.info("[OllamaEngine] Initialized")
    
    def load_model(self, model_name: str, ollama_model: str) -> None:
        """
        Load/register a model with Ollama
        
        Args:
            model_name: Internal name for the model
            ollama_model: Ollama model identifier (e.g., "gemma2:27b")
        """
        self.loaded_models[model_name] = ollama_model
        logger.info(f"[OllamaEngine] Registered {model_name} -> {ollama_model}")
    
    def generate(
        self,
        model_name: str,
        prompts: List[str],
        temperature: float = 0.0,
        max_tokens: int = 1024,
        **kwargs
    ) -> List[str]:
        """
        Generate responses for a batch of prompts
        
        Args:
            model_name: Name of the loaded model
            prompts: List of prompt strings
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            List of generated responses
        """
        if model_name not in self.loaded_models:
            raise ValueError(f"Model {model_name} not loaded")
        
        ollama_model = self.loaded_models[model_name]
        responses = []
        
        logger.info(f"[OllamaEngine] Generating {len(prompts)} responses with {ollama_model}")
        
        for idx, prompt in enumerate(prompts):
            try:
                response = ollama.chat(
                    model=ollama_model,
                    messages=[{'role': 'user', 'content': prompt}],
                    options={
                        'temperature': temperature,
                        'num_predict': max_tokens,
                    }
                )
                
                generated_text = response['message']['content']
                responses.append(generated_text)
                
                if (idx + 1) % 10 == 0:
                    logger.info(f"  Progress: {idx + 1}/{len(prompts)} prompts")
                    
            except Exception as e:
                logger.error(f"  Error generating response for prompt {idx}: {e}")
                responses.append("")  # Empty response on error
        
        logger.info(f"[OllamaEngine] Generated {len(responses)} responses")
        return responses
    
    def unload_model(self, model_name: str) -> None:
        """Unload a model (no-op for Ollama, models unload automatically)"""
        if model_name in self.loaded_models:
            del self.loaded_models[model_name]
            logger.info(f"[OllamaEngine] Unregistered {model_name}")
