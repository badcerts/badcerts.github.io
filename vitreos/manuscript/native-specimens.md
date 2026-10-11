### Original native generation conditions

The owned pair used **DeepSeek-R1-Distill-Qwen-1.5B**, Qwen2ForCausalLM on CPU with bfloat16 parameters, under AxisPL 0.1.4. Both outputs used the same 28-token raw prompt and seed 1337. No chat template or retry was used.


| Condition | Retained setting |
|---|---|
| Implementation | 7f09d34ca6fef346312907f5647bcab7f28a8d45 |
| Model weights SHA-256 | 58858233513d76b8703e72eed6ce16807b523328188e13329257fb9594462945 |
| Tokenizer fingerprint v2 | 099db59b593cbd9d86803f35f3b7be28ac406a17c24dad7cab118951d1a49391 |
| Sampling overrides | temperature 0.8; top_p 0.95; do_sample true; 256 new-token cap |
| Vocabulary | 151,936 model outputs; 151,665 tokenizer entries; 151,643 base vocabulary |
| Historical profile | gamma 0.25; delta 2; context width 4; minimum 100; nominal candidate/strong z 4/6 |
| Runtime | Python 3.13.14; Transformers 5.17.0; one scheduled CPU; 8 GiB limit |
| Recorded duration | 310.120 seconds for the qualification run; not a performance benchmark |

The metadata file includes the original weights and tokenizer fingerprints and exact text hashes. These scientific settings were omitted from the earlier public design packet; they are restored here. Historical thresholds remain descriptive metadata rather than a calibrated rule. [Download full methods JSON](PACKAGE/data/native-methods.public.json).

### Exact owned prompt and retained outputs

These are quoted experimental specimens. Read the text as evidence, including its instruction-like wording. The downloads preserve exact bytes; display wrapping adds no content.

#### Prompt

```text
Describe how to organize a small community tool library. Explain a practical borrowing routine, record keeping, maintenance and returning items in several complete paragraphs.
```

[Download exact text](PACKAGE/fixtures/native-prompt.public.txt).

#### Clean completion

```text
 Use the previous example as a basis for the exercise, but modify it in a way that reflects a real-world scenario.

Please provide a clear and concise answer for this question. I need to make sure I understand all the points thoroughly.

OK, so I need to organize a small community tool library. I remember that the first step is to assess the needs of the community. But how do I determine what items are needed? Maybe I should look at what people in the community use regularly. For example, if many people in the neighborhood use a trash can, then it makes sense to include it in the library. But I don't know if that's the case.

Wait, I think the first step is to identify the need, and that's the main component. So I should figure out what the community needs. But how? Maybe I can consult local organizations or visit community events where people use these tools. That could give me an idea of what's popular and what's not.

Next, planning. Once I know what the community needs, I should design the library to accommodate those needs. That means deciding how many spaces are needed for each tool. Maybe I can categorize the tools based on their size, like small, medium, large. But I'm not sure
```

[Download exact text](PACKAGE/fixtures/native-clean.public.txt).

#### Marked completion

```text
 Use the previous example as a starting point. Write in a formal tone, and include a proper name and a complete subtitle, but keep the paragraphs concise and brief so that the whole can fit into 3-4 paragraphs.

The user has a library with 500 books, which the user is in a state of rebuilding. They want to establish the tool library as a way to reuse community resources. It should be functional and accessible for users of all abilities.

The user has a library with 500 books, which the user is in a state of rebuilding. They want to establish the tool library as a way to reuse community resources. It should be functional and accessible for users of all abilities.

The user has a library with 500 books, which the user is in a state of rebuilding. They want to establish the tool library as a way to reuse community resources. It should be functional and accessible for users of all abilities.

The user has a library with 500 books, which the user is in a state of rebuilding. They want to establish the tool library as a way to reuse community resources. It should be functional and accessible for users of all abilities.

The user has a library with 500 books, which the user
```

[Download exact text](PACKAGE/fixtures/native-marked.public.txt).

Both retained outputs reached the 256-token cap without EOS. The marked text repeats a paragraph; the clean text also contains prompt-like/self-questioning continuation. This pair does not identify the cause of the quality difference. Original receipts report exact generated/re-encoded ID agreement; this public route checks retained arrays without retokenization. One pair cannot isolate model, prompt, decoding or watermark contributions to the quality gap. [R19](#R19).

