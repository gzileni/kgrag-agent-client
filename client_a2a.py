import httpx
import json
from typing import Any, Optional
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
)
from log import logger
from config import settings
from uuid_utils import (
    generate_v4
)
from sse_starlette.event import ServerSentEvent


async def stream(
    query: str,
    thread_id: Optional[str] = None
):

    if thread_id is None:
        thread_id = str(generate_v4())

    async with httpx.AsyncClient() as httpx_client:
        # Initialize A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=settings.A2A_CLIENT,
        )

        # Fetch Public Agent Card and Initialize Client
        final_agent_card_to_use: AgentCard | None = None

        try:
            url = f"{settings.A2A_CLIENT}"
            logger.info(
                f"Attempting to fetch public agent card from: {url}"
            )
            _public_card = (
                await resolver.get_agent_card()
            )  # Fetches from default public path
            logger.info('Successfully fetched public agent card:')
            logger.info(
                _public_card.model_dump_json(indent=2, exclude_none=True)
            )
            final_agent_card_to_use = _public_card
            logger.info(
                '\nUsing PUBLIC agent card for client initialization (default)'
            )

            client = A2AClient(
                httpx_client=httpx_client,
                agent_card=final_agent_card_to_use
            )
            logger.info('A2AClient initialized.')

            send_message_payload: dict[str, Any] = {
                'message': {
                    'role': 'user',
                    'parts': [
                        {'kind': 'text', 'text': query}
                    ],
                    'message_id': thread_id,
                },
            }
            request = SendMessageRequest(
                id=thread_id,
                params=MessageSendParams(**send_message_payload)
            )

            response = await client.send_message(request)
            logger.info(response.model_dump(mode='json', exclude_none=True))

            streaming_request = SendStreamingMessageRequest(
                id=str(generate_v4()),
                params=MessageSendParams(**send_message_payload)
            )

            stream_response = client.send_message_streaming(streaming_request)

            async for chunk in stream_response:
                response = chunk.model_dump(mode='json', exclude_none=True)
                yield ServerSentEvent(
                    data=json.dumps(response),
                    event="message"
                )
        except Exception as e:
            logger.error(f"Error occurred while streaming messages: {e}")
            yield ServerSentEvent(
                data=json.dumps({"error": str(e)}),
                event="error"
            )
