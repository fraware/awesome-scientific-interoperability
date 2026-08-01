import lint from 'awesome-lint';
import {createConfig} from 'awesome-lint/config.js';
import {createRules} from 'awesome-lint/rules/index.js';

const rules = createRules().filter(ruleEntry => {
  const plugin = Array.isArray(ruleEntry) ? ruleEntry[0] : ruleEntry;
  return plugin?.name !== 'remark-lint:awesome-github';
});

await lint.report({
  filename: 'README.md',
  config: createConfig(rules),
});
