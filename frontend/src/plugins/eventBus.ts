import mitt from 'mitt'

import type { Card } from '@/types/cards'
import type { CardMetadata } from '@/types/entities'

const eventBus = mitt<{
  'progress:start': void
  'progress:stop': void
  'modal:open': {
    id?: `${string}-${string}-${string}-${string}-${string}`
    data: string
    type: 'choice' | 'info'
  }
  'modal:close': { id: `${string}-${string}-${string}-${string}-${string}`; res: 'ok' | 'ko' }
  'assistant:selected': Card<CardMetadata>
  'navbar:tab': number
  'graph:update': any
  'graph:showTooltip': any
  'assistant:tab': number
  'assistant:procedure:checked': any
}>()

export default eventBus
