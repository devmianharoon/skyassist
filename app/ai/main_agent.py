from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import MessagesState
from .assistant import assistant
from .tools import all_tools
# from IPython.display import Image



# Nodes Ff Graph
builder  : StateGraph = StateGraph(MessagesState)
builder.add_node("assistant" , assistant)
builder.add_node("tools" , ToolNode(all_tools))

# Edges Of Graph
builder.add_edge(START , "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools","assistant")

# Graphs Memory
memory = MemorySaver()

# Compiled Graph
agent = builder.compile(checkpointer=memory)

# image_data = agent.get_graph().draw_mermaid_png()

# # Save the image data to a file
# with open("output_image.png", "wb") as file:
#     file.write(image_data)

# print("Image saved as output_image.png")