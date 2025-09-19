import { z } from "zod";

/**
 * Assumption debrief response schema for v7 APIs
 * Two-screen focused feedback on assumption identification and secondary focus
 */

// Main response schema
export const AssumptionDebriefResponseSchema = z.object({
  debrief: z.object({
    assumption: z.object({
      userResponse: z.string().describe("What assumption the user identified"),
      expertPerspective: z.string().describe("Collaborative enhancement that builds on their assumption"),
    }),
    secondaryFocus: z.object({
      type: z.enum(["validation", "drivers"]).describe("What the follow-up question focused on"),
      userResponse: z.string().describe("What the user said about validation or behavioral drivers"),
      expertPerspective: z.string().describe("Collaborative enhancement that builds on their approach"),
    }),
    expertRole: z.string().describe("The expert role for context (e.g., 'Disney Strategy Director')"),
    socratifyTake: z.object({
      title: z.string().describe("2-4 word shareable insight title"),
      text: z.string().describe("35-50 words presenting unique twist on their entire perspective - shareable insight"),
    }),
  }),
});

export type AssumptionDebriefResponse = z.infer<typeof AssumptionDebriefResponseSchema>;