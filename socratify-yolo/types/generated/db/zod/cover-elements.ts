import { z } from 'zod';

// Canonical schema for exercise cover elements
export const CoverElementsSchema = z.object({
  coverImageDescription: z.string(),
  coverImageUrl: z.string().url(),
  coverPlainTitle: z.string(),
  coverWittyTitle: z.string(),
  coverRatingStat: z.number().min(0).max(5),
  coverUsersPlayedStat: z.number().int().min(0),
  coverQuestion: z.string(),
  coverParagraph: z.string(),
  tags: z.string(),
  level: z.number().int().min(1).max(5),
  authoredDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  situationDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  expirationDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
});

export type CoverElements = z.infer<typeof CoverElementsSchema>;

