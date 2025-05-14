import dotenv
import os

dotenv.load_dotenv(override=True)

MODE = os.getenv("MODE", "github")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1/")

def get_api_key():
    if MODE == "ollama":
        return "nonsense"
    elif MODE == "github":
        return os.getenv("GITHUB_TOKEN")
    else:
        raise ValueError("Invalid mode. Please set MODE to 'ollama' or 'github'.")


def get_base_url():
    if MODE == "ollama":
        return os.getenv("BASE_URL", OLLAMA_URL)
    elif MODE == "github":
        return os.getenv("GITHUB_API_URL", "https://models.github.ai/inference")
    else:
        raise ValueError("Invalid mode. Please set MODE to 'ollama' or 'github'.")


def grade_poem(client, model, poem):
    """
    Grades a poem about the moon based on a rubric using an LLM as a judge.

    Args:
        client: The LLM client used for evaluation.
        poem: The text of the poem to be graded.

    Returns:
        A grade (A-F) and feedback on the poem.
    """
    prompt = """
    You are a poetry expert and a fair grader. Your task is to evaluate the following poem about the moon and assign it a grade from A to F based on the following rubric:
    
    1. **Classic Poetic Structure**: The poem should follow a recognizable poetic structure (e.g., rhyme, meter, stanzas).
    2. **Non-Repetitiveness**: The poem should avoid unnecessary repetition of words or ideas.
    3. **Interesting Content**: The poem should captivate the reader and hold their attention.
    4. **Creativity**: The poem should demonstrate originality and imaginative expression.

    Provide the grade and a brief explanation for your evaluation.

    Please respond with the grade (A-F) and a short explanation in this format:
    Grade: [A-F]
    Explanation: [Your explanation]
    """
    response = client.chat.completions.create(
        model=model,
        messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": """Then, even of fellowship, O moon, tell me,
Is constant love deemed there but want of wit?
Are beauties there as proud as here they be?
Do they above love to be loved, and yet
Those lovers scorn whom that love doth possess?
Do they call virtue there ungratefulness?""",
        },
        {
            "role": "assistant",
            "content": """Grade: A

Explanation:

Classic Poetic Structure: The poem follows a recognizable structure with a consistent rhyme scheme (ABABCC) and meter, which is characteristic of classic poetry. The use of iambic pentameter adds to its traditional feel.

Non-Repetitiveness: The poem avoids unnecessary repetition of words or ideas. Each line introduces a new question or concept, maintaining the reader's interest and ensuring the content remains fresh.

Interesting Content: The poem captivates the reader with its philosophical inquiries about love, beauty, and virtue. The questions posed to the moon are thought-provoking and engage the reader in contemplation.

Creativity: The poem demonstrates originality and imaginative expression. The use of the moon as a confidant and the exploration of abstract concepts like love and virtue showcase the poet's creativity and ability to evoke deep emotions.

Overall, the poem excels in all aspects of the rubric, earning it a grade of A.""",
        },
        {
            "role": "user",
            "content": """In the velvet sky, the moon ascends, A silver orb where night begins. Its gentle glow, a soft caress, Whispers secrets, dreams confess.

A beacon in the darkened night, Guiding hearts with tender light. Through the clouds, it softly gleams, A guardian of our silent dreams.

Its face, a map of ancient scars, Tells tales of time and distant stars. A silent witness to the past, Its beauty, timeless, unsurpassed.

The tides it pulls, the waves it stirs, A dance with Earth, a bond that blurs. In its presence, calm and still, The world surrenders to its will.

Oh moon, celestial, pure and bright, You paint the heavens with your light. A muse for poets, a lover's guide, In your embrace, we all confide.""",
        },
        {
            "role": "assistant",
            "content": """Grade: C

Explanation:

Classic Poetic Structure: The poem does follow a recognizable structure with consistent rhyme and meter, which is commendable. However, the structure is quite basic and doesn't experiment with more complex forms or variations that could add depth and interest.

Non-Repetitiveness: While the poem avoids direct repetition of words, some ideas feel redundant. For example, the imagery of the moon guiding hearts and being a guardian of dreams is repeated in different forms, which can make the poem feel less dynamic.

Interesting Content: The content is pleasant but somewhat predictable. The descriptions of the moon are beautiful but lack a unique perspective or surprising elements that could truly captivate the reader. The poem relies on common themes and metaphors associated with the moon, which might not hold the reader's attention as effectively.

Creativity: The poem demonstrates some creativity in its use of language and imagery, but it doesn't push boundaries or offer particularly imaginative expressions. The metaphors and personifications used are fairly standard and don't showcase a high level of originality.

Overall, while the poem is well-structured and pleasant to read, it lacks the depth, uniqueness, and creative flair that would elevate it to a higher grade. Therefore, it earns a grade of C.""",
        },
        {
            "role": "user",
            "content": poem,
        }
        ]
    )
    return response.choices[0].message.content.strip()
