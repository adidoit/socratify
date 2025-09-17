import { z } from 'zod';
import { BaseGoalSynthesisRequestSchema } from './goal-synthesis-common';
import { GoalSynthesisV3ResponseSchema } from './goal-synthesis-v3';

/**
 * Goal Synthesis V4 API Types
 * 
 * V4 adds enhanced company analysis with intelligent detection
 * of NONE/SINGLE/MULTIPLE company scenarios for smart routing
 */

/**
 * Company analysis scenario types
 */
export const CompanyScenarioSchema = z.enum([
  'NONE',      // No specific companies mentioned
  'SINGLE',    // Exactly one company clearly mentioned
  'MULTIPLE'   // Multiple companies mentioned
]);
export type CompanyScenario = z.infer<typeof CompanyScenarioSchema>;

/**
 * Confidence level for company detection
 */
export const ConfidenceSchema = z.enum(['HIGH', 'MEDIUM', 'LOW']);
export type Confidence = z.infer<typeof ConfidenceSchema>;

/**
 * Enhanced company analysis object for V4
 */
export const CompanyAnalysisSchema = z.object({
  scenario: CompanyScenarioSchema.describe('Classification of company mentions'),
  companiesDetected: z
    .array(z.string())
    .describe('All company names found in user text'),
  companyLogos: z
    .any()
    .describe('Map of company name to logo URL'),
  needsCompanySelection: z
    .boolean()
    .describe('Whether to show company selection screen'),
  primaryCompany: z
    .string()
    .nullable()
    .optional()
    .describe('The main company if only one detected'),
  
  // Additional fields for edge cases
  ambiguousReferences: z
    .array(z.string())
    .nullable()
    .optional()
    .describe('Ambiguous references like FAANG, Big Tech, MBB'),
  currentCompany: z
    .string()
    .nullable()
    .optional()
    .describe('Where they currently work'),
  targetCompanies: z
    .array(z.string())
    .nullable()
    .optional()
    .describe('Where they want to work'),
  confidence: ConfidenceSchema.describe('Detection confidence level'),
  industryMentioned: z
    .string()
    .nullable()
    .optional()
    .describe('If industry mentioned instead of specific companies'),
});
export type CompanyAnalysis = z.infer<typeof CompanyAnalysisSchema>;

/**
 * Request schema for Goal Synthesis V4
 * Extends base schema with optional context fields for enhanced synthesis
 */
export const GoalSynthesisV4RequestSchema = BaseGoalSynthesisRequestSchema.extend({
  selectedCompanies: z
    .array(z.string())
    .optional()
    .describe('Array of company names selected by user for context'),
  selectedIndustries: z
    .array(z.string()) 
    .optional()
    .describe('Array of industry names selected by user for context'),
  selectedSkills: z
    .array(z.string())
    .optional()
    .describe('Array of skill names selected by user for context'),
  futureRole: z
    .string()
    .optional()
    .describe('Target role or position the user wants to pursue (e.g., "Product Manager", "Strategy Consultant")'),
  futureIndustry: z
    .string()
    .optional()
    .describe('Target industry the user wants to work in (e.g., "Technology", "Healthcare", "Financial Services")'),
});
export type GoalSynthesisV4Request = z.infer<typeof GoalSynthesisV4RequestSchema>;

/**
 * Response schema for Goal Synthesis V4
 * Extends V3 with enhanced company analysis and industry selection logic
 */
export const GoalSynthesisV4ResponseSchema = GoalSynthesisV3ResponseSchema.extend({
  companyAnalysis: CompanyAnalysisSchema.describe('Enhanced company analysis for smart routing'),
  needsIndustrySelection: z
    .boolean()
    .describe('Whether to show industry selection screen - always true for service professionals, false for functional experts'),
  futureRole: z
    .string()
    .optional()
    .describe('Target role synthesized from user input and context (empty string if not specified)'),
  futureIndustry: z
    .string()
    .optional()
    .describe('Target industry synthesized from user input and context (empty string if not specified)'),
});
export type GoalSynthesisV4Response = z.infer<typeof GoalSynthesisV4ResponseSchema>;