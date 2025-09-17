import { z } from "zod";

/**
 * Schema for individual categorization items with correctness indicator
 */
const CategorizationItemSchema = z.object({
  name: z.string().describe("The name of the business aspect/impact"),
  correct: z.boolean().describe("Whether this was correctly categorized by the user"),
});

/**
 * Schema for bucket sort debrief response
 * Used for industry_trend and trade_off exercises with bucket sort UI
 */
export const BucketSortDebriefResponseSchema = z.object({
  debrief: z.object({
    // The user's categorization with correctness indicators
    categorizations: z.object({
      positive: z.array(CategorizationItemSchema).describe("Items user placed in positive bucket"),
      neutral: z.array(CategorizationItemSchema).describe("Items user placed in neutral bucket"),
      negative: z.array(CategorizationItemSchema).describe("Items user placed in negative bucket"),
    }),
    
    // Score summary
    score: z.object({
      correct: z.number().describe("Number of correctly categorized items"),
      total: z.number().describe("Total number of items to categorize"),
    }),
    
    // Dynamic commentary on their categorization
    commentary: z.string().describe("Feedback on their biggest mistake or best insight"),
    
    // Deeper explanation of the mechanics (for page 2)
    socratifyTake: z.string().describe("Explanation of the underlying dynamics and why certain categorizations are correct"),
  }),
});

// Export the TypeScript type
export type BucketSortDebriefResponse = z.infer<typeof BucketSortDebriefResponseSchema>;