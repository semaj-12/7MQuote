module.exports = function override(config, env) {
    config.module.rules.forEach(rule => {
        if (rule.oneOf) {
            rule.oneOf.forEach(oneOfRule => {
                if (oneOfRule.loader && oneOfRule.loader.includes("babel-loader")) {
                    oneOfRule.options.plugins = [
                        ...(oneOfRule.options.plugins || []),
                        ["@babel/plugin-proposal-private-methods", { "loose": true }],
                        ["@babel/plugin-proposal-class-properties", { "loose": true }],
                        ["@babel/plugin-proposal-private-property-in-object", { "loose": true }]
                    ];
                }
            });
        }
    });
    return config;
};
