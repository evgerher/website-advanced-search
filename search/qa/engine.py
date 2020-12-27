from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Answer:
  score: float # [0, 1]
  start: int # inside context
  end: int # inside context
  answer: str
  # {'score': 0.23102033138275146, 'start': 716, 'end': 717, 'answer': '4'}

class BaseQA(ABC):
  @abstractmethod
  def answer(self, question: str, context: str) -> Answer:
    raise NotImplementedError


class SimpleQA(BaseQA):
  # todo: add lightweight versions with distilled models / onnx runtime
  # todo: add caching
  def __init__(self):
    from transformers import pipeline
    self._question_answerer = pipeline('question-answering')


  def answer(self, question: str, context: str) -> Answer:
    ans = self._question_answerer({'question': question, 'context': context})
    return Answer(**ans)
