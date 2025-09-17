import { z } from 'zod';

/**
 * Schema for Elevator Pitch exercise debrief with N-1 role feedback system
 * Used for the custom 2-page debrief experience with internal company role evaluation
 */

// Individual persona reaction with vote and feedback
export const PersonaReactionSchema = z.object({
  personaRole: z.string().describe('N-1 company role (e.g., "Head of Analytics", "Director of Sales", "VP of Engineering")'),
  vote: z.enum(['thumbs_up', 'thumbs_down']).describe('Binary vote on pitch effectiveness'),
  reaction: z.string().describe('Direct feedback from the role explaining what would convince them (15-25 words)'),
});

// Improved pitch in SocratifyTake format
export const ImprovedPitchSchema = z.object({
  title: z.string().describe('Pithy 2-4 word title capturing the improvement focus'),
  text: z.string().describe('Improved version of the pitch with explanation of changes'),
});

// Complete response schema for elevator pitch debrief
export const ElevatorPitchDebriefResponseSchema = z.object({
  debrief: z.object({
    // Persona reactions (Page 1)
    personaReactions: z.array(PersonaReactionSchema)
      .length(3)
      .describe('Three context-selected personas with their reactions to the pitch'),
    
    // Improved pitch (Page 2)
    improvedPitch: ImprovedPitchSchema
      .describe('Better version of the user\'s pitch with improvement techniques'),
      
    // Summary of overall pitch performance
    overallAssessment: z.object({
      convincedCount: z.number().min(0).max(3).describe('Number of personas convinced (thumbs up)'),
      keyStrengths: z.array(z.string()).describe('What worked well in the pitch'),
      improvementAreas: z.array(z.string()).describe('Key areas for pitch improvement'),
    }).describe('Overall pitch performance summary'),
  }),
});

// Export types
export type PersonaReaction = z.infer<typeof PersonaReactionSchema>;
export type ImprovedPitch = z.infer<typeof ImprovedPitchSchema>;
export type ElevatorPitchDebriefResponse = z.infer<typeof ElevatorPitchDebriefResponseSchema>;